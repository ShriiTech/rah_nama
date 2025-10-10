import re
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from account.models.custom_user import CustomUser


class PhoneTokenObtainSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_phone_number(self, value):
        """
        نرمال‌سازی و اعتبارسنجی شماره تلفن:
        - اگر با 0 شروع شده → جایگزین با +98
        - باید با +98 شروع شود
        - فقط اعداد بعد از +98 مجاز هستند
        - باید دقیقاً 13 کاراکتر باشد (مثل +989121234567)
        """
        value = value.strip()

        if value.startswith("0"):
            value = "+98" + value[1:]

        if not value.startswith("+98"):
            raise serializers.ValidationError("Phone number must start with +98.")

        if not re.fullmatch(r"^\+98\d{10}$", value):
            raise serializers.ValidationError("Phone number format is invalid. Example: +989121234567")

        return value

    def validate(self, attrs):
        phone_number = self.validate_phone_number(attrs.get("phone_number", ""))
        password = attrs.get("password")

        if not password:
            raise serializers.ValidationError({"detail": "Password is required."})

        try:
            user = CustomUser.objects.get(phone_number=phone_number)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"detail": "Invalid credentials."})

        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "Invalid credentials."})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "User account is inactive."})

        # تولید JWT Tokens
        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_id": user.pk,
            "phone_number": user.phone_number,
        }

    class Meta:
        fields = ["phone_number", "password"]
