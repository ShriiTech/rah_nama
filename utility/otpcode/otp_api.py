import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.conf import settings

from utility.otpcode.otp_serializer import RequestOTPSerializer
from utility.otpcode.otp import (
    generate_otp, cache_otp, get_cached_otp, invalidate_otp,
    increment_request_count, get_request_count
)

# --- تنظیم Logger ---
logger = logging.getLogger(__name__)

# Placeholder برای ارسال پیامک — جایگزین کنید با سرویس SMS واقعی
def send_sms(phone_number: str, message: str):
    try:
        # اینجا کد واقعی ارسال پیامک قرار می‌گیرد
        print(f"[SMS SEND] to={phone_number} message={message}")
        logger.info(f"SMS sent to {phone_number}: {message}")
    except Exception as e:
        logger.error(f"SMS sending failed to {phone_number}: {e}")


class RequestOTPAPIView(APIView):
    """
    POST: { "phone_number": "+98912XXXXXXX" }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestOTPSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Invalid OTP request data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone = serializer.validated_data["phone_number"]
        logger.info(f"OTP request received for phone {phone}")

        # rate limit ساده
        max_req = getattr(settings, "OTP_MAX_REQUESTS", 10)
        count = increment_request_count(phone)
        logger.debug(f"OTP request count for {phone}: {count}/{max_req}")

        if count > max_req:
            logger.warning(f"Rate limit exceeded for {phone}")
            return Response(
                {"detail": "تعداد درخواست‌های OTP برای این شماره بیش از حد مجاز است. بعداً تلاش کنید."},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        otp = generate_otp(6)
        cache_otp(phone, otp)
        logger.info(f"OTP generated and cached for {phone}")

        try:
            send_sms(phone, f"کد تأیید شما: {otp}. این کد تا {getattr(settings,'OTP_TTL',300)//60} دقیقه معتبر است.")
        except Exception as e:
            logger.error(f"Error sending OTP SMS to {phone}: {e}")
            return Response({"detail": "خطا در ارسال پیامک."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"detail": "کد OTP ارسال شد." , "otp": otp}, status=status.HTTP_200_OK)


