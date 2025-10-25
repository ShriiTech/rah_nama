import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from drf_spectacular.utils import extend_schema_view

from account.models import CustomUser
from account.schema.auth.jwt.otp import VerifyOTPSchema
from account.serializers.auth.jwt.otp import VerifyOTPSerializer
from utility.otp_code import OTPService

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=VerifyOTPSchema.post(),
)
class VerifyOTPAPIView(APIView):
    """
    API endpoint for verifying OTP codes.
    Validates OTPs via Redis using OTPService, creates users if needed,
    and returns JWT access/refresh tokens.
    """
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Invalid OTP verification data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data["phone_number"]
        otp = serializer.validated_data["otp"].strip()

        logger.info(f"OTP verification attempt for {phone}")

        otp_service = OTPService()

        # ✅ Verify OTP using Redis-backed service
        try:
            if not otp_service.verify_otp(phone, otp):
                logger.warning(f"Incorrect or expired OTP for {phone}")
                return Response(
                    {"detail": "کد وارد شده اشتباه یا منقضی شده است."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            logger.error(f"Error verifying OTP for {phone}: {e}", exc_info=True)
            return Response(
                {"detail": "خطا در تأیید کد. لطفاً بعداً تلاش کنید."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # ✅ OTP verified successfully — create or activate user
        user, created = CustomUser.objects.get_or_create(
            phone_number=phone,
            defaults={"is_active": True},
        )

        # ✅ Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        logger.info(f"OTP verified successfully for {phone}")

        return Response(
            {
                "access": access,
                "refresh": str(refresh),
                "detail": "ورود با موفقیت انجام شد.",
            },
            status=status.HTTP_200_OK,
        )
