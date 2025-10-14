import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from django.conf import settings

from account.models import CustomUser
from account.serializers.auth.jwt.otp import VerifyOTPSerializer
from utility.otpcode.otp import get_cached_otp, invalidate_otp


logger = logging.getLogger(__name__)


class VerifyOTPAPIView(APIView):
    """
    POST: { "phone_number": "+98912XXXXXXX", "otp": "123456" }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Invalid OTP verification data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data["phone_number"]
        otp = serializer.validated_data["otp"].strip()

        logger.info(f"OTP verification attempt for {phone}")

        cached = get_cached_otp(phone)
        if cached is None:
            logger.warning(f"OTP expired or missing for {phone}")
            return Response({"detail": "کد منقضی شده یا وجود ندارد."}, status=status.HTTP_400_BAD_REQUEST)

        if otp != cached:
            logger.warning(f"Incorrect OTP entered for {phone}")
            return Response({"detail": "کد اشتباه است."}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ در صورت معتبر بودن OTP:
        invalidate_otp(phone)

        # ✅ اگر کاربر قبلاً وجود ندارد، بسازش
        user, created = CustomUser.objects.get_or_create(
            phone_number=phone,
            defaults={
                "is_active": True,
            }
        )

        # ✅ تولید توکن JWT
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        logger.info(f"OTP verified successfully for {phone}")

        return Response({
            "access": access,
            "refresh": str(refresh),

        }, status=status.HTTP_200_OK)
