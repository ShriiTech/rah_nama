from rest_framework import serializers
from account.models.custom_user import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", "phone_number", "email", "first_name", "last_name",
            "is_active", "is_staff", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "password": {"write_only": True}
        }