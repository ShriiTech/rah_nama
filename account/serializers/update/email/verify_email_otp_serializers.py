from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from utility.otpcode.otp import get_cached_otp, invalidate_otp

customuser = get_user_model()

class VerifyEmailOTPSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user = self.context["request"].user
        new_email = attrs["new_email"]
        user_otp_code = attrs["otp_code"]

        redis_key = f"email_otp:{user.id}:{new_email}"

        cached_otp_code = get_cached_otp(redis_key)
        if not cached_otp_code:
            raise serializers.ValidationError(_("Verification code expired or not found."))

        if cached_otp_code != user_otp_code:
            raise serializers.ValidationError(_("Invalid verification code."))

        attrs["new_email"] = new_email
        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        new_email = self.validated_data["new_email"]

        user.email = new_email
        user.save(update_fields=["email"])

        # پاک‌کردن OTP بعد از تأیید موفق
        invalidate_otp(new_email)

        return user
