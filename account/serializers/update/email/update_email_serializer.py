# accounts/serializers.py
from django.core.cache import cache
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from utility.otpcode.otp import  cache_otp, generate_otp


customuser = get_user_model()


class RequestEmailChangeSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_email = serializers.EmailField()
    new_email_confirm = serializers.EmailField()

    OTP_TTL = 600  # 10 دقیقه (به ثانیه)

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Password is incorrect."))
        return value

    def validate(self, attrs):
        new_email = attrs['new_email']
        confirm = attrs['new_email_confirm']
        user = self.context['request'].user

        if new_email != confirm:
            raise serializers.ValidationError({"new_email_confirm": _("Emails do not match.")})

        if customuser.objects.filter(email__iexact=new_email).exists():
            raise serializers.ValidationError({"new_email": _("This email is already in use.")})

        # اگر OTP هنوز معتبره، خطا بده تا spam نشه
        otp_key = f"email_otp:{user.id}:{new_email}"
        if cache.get(otp_key):
            raise serializers.ValidationError(_("A verification code was already sent. Please wait before retrying."))

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        new_email = validated_data['new_email']

        otp_code = generate_otp(6)
        otp_key = f"email_otp:{user.id}:{new_email}"

        # ذخیره در Redis
        cache_otp(new_email, otp_code, ttl=self.OTP_TTL)
        # ارسال ایمیل (می‌تونی با Celery غیرهمزمانش کنی)
        send_mail(
            subject="Email change verification code",
            message=f"Your verification code is: {otp_code}",
            from_email="no-reply@example.com",
            recipient_list=[new_email],
            fail_silently=False,
        )

        return {"email": new_email, "otp_sent": True}
