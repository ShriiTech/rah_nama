from rest_framework import serializers
import re


PHONE_RE = re.compile(r'^\+?[0-9]{10,15}$')  # ساده؛ در صورت نیاز stricter کنید


class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    otp = serializers.CharField(max_length=10)
