from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


class PasswordLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        if not phone_number or not password:
            raise serializers.ValidationError("Phone number and password are required")

        user = authenticate(phone_number=phone_number, password=password)

        if not user:
            raise AuthenticationFailed("Invalid phone number or password")

        if not user.is_active:
            raise AuthenticationFailed("This account is inactive")

        data["user"] = user
        return data
