from rest_framework import serializers
import re

PHONE_RE = re.compile(r'^\+?[0-9]{10,15}$')  # ساده؛ در صورت نیاز stricter کنید

class RequestOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        v = value.strip()
        if not PHONE_RE.match(v):
            raise serializers.ValidationError("فرمت شماره تلفن معتبر نیست. از فرمت بین‌المللی مانند +98912... استفاده کنید.")
        return v
