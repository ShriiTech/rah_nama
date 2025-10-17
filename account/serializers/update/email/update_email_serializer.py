import logging
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from utility.otpcode.otp import cache_otp, generate_otp

customuser = get_user_model()

# تعریف logger
logger = logging.getLogger(__name__)

class RequestEmailChangeSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_email = serializers.EmailField()
    new_email_confirm = serializers.EmailField()

    OTP_TTL = 600  # 10 دقیقه (به ثانیه)

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            logger.warning(f"User {user.id} entered incorrect password for email change.")
            raise serializers.ValidationError(_("Password is incorrect."))
        logger.debug(f"User {user.id} password validated successfully.")
        return value

    def validate(self, attrs):
        new_email = attrs['new_email']
        confirm = attrs['new_email_confirm']
        user = self.context['request'].user

        if new_email != confirm:
            logger.warning(f"User {user.id} email confirmation does not match. new_email={new_email}")
            raise serializers.ValidationError({"new_email_confirm": _("Emails do not match.")})

        if customuser.objects.filter(email__iexact=new_email).exists():
            logger.info(f"User {user.id} tried to change email to an already used email: {new_email}")
            raise serializers.ValidationError({"new_email": _("This email is already in use.")})

        redis_key = f"email_otp:{user.id}:{new_email}"
        if cache.get(redis_key):
            logger.info(f"User {user.id} tried to request OTP for {new_email} but OTP is still valid.")
            raise serializers.ValidationError(_("A verification code was already sent. Please wait before retrying."))

        logger.debug(f"User {user.id} email change validation passed for new_email={new_email}")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        new_email = validated_data['new_email']

        otp_code = generate_otp(6)
        redis_key = f"email_otp:{user.id}:{new_email}"

        # ذخیره در Redis
        cache_otp(redis_key, otp_code, ttl=self.OTP_TTL)
        logger.info(f"OTP code ({otp_code}) generated for user {user.id} to change email to {new_email}")

        # ارسال ایمیل
        try:
            send_mail(
                subject="Email change verification code",
                message=f"Your verification code is: {otp_code}",
                from_email="rah.nama.drf@gmail.com",
                recipient_list=[new_email],
            )
            logger.info(f"Verification email sent to {new_email} for user {user.id}")
        except Exception as e:
            logger.error(f"Failed to send verification email to {new_email} for user {user.id}: {e}")
            raise serializers.ValidationError(_("Failed to send verification email. Please try again later."))

        return {"email": new_email, "otp_sent": True}
