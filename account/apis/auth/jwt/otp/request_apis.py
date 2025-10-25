import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.core.exceptions import ValidationError

from account.schema.auth.jwt.otp import RequestOTPSchema
from account.serializers.auth.jwt.otp import RequestOTPSerializer
from utility.otp_code import OTPService
from drf_spectacular.utils import extend_schema_view

logger = logging.getLogger(__name__)


@extend_schema_view(
    post=RequestOTPSchema.post(),
)
class RequestOTPAPIView(APIView):
    """
    API endpoint for requesting a One-Time Password (OTP).
    Handles rate limiting, OTP generation, and caching via Redis.
    """
    permission_classes = [AllowAny]
    serializer_class = RequestOTPSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Invalid OTP request data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data["phone_number"]
        logger.info(f"OTP request received for phone {phone}")

        otp_service = OTPService()

        try:
            # Generate and cache OTP (includes rate-limit check)
            otp = otp_service.generate_and_cache_otp(phone)
            logger.info(f"OTP generated and cached for {phone}")

            # TODO: integrate actual SMS sending logic here if needed
            # sms_service.send_otp(phone, otp)

            return Response(
                {"detail": "کد OTP ارسال شد.", "otp": otp},
                status=status.HTTP_200_OK
            )

        except ValidationError as e:
            logger.warning(f"Rate limit exceeded for {phone}: {str(e)}")
            return Response(
                {"detail": "تعداد درخواست‌های OTP برای این شماره بیش از حد مجاز است. بعداً تلاش کنید."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        except Exception as e:
            logger.error(f"Unexpected error while processing OTP for {phone}: {e}", exc_info=True)
            return Response(
                {"detail": "خطا در پردازش درخواست. لطفاً بعداً تلاش کنید."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
