from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from utility.otp_code import OTPService


otp_service = OTPService()


class VerifyEmailUpdateSerializer(serializers.Serializer):
    new_email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user = self.context["request"].user
        new_email = attrs["new_email"]
        user_otp_code = attrs["otp_code"]

        is_cached_otp_code = otp_service.verify_otp(user.phone_number, user_otp_code)

        if not is_cached_otp_code:
            raise serializers.ValidationError(_("Invalid verification code."))

        return attrs
