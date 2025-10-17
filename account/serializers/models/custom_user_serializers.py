from rest_framework import serializers
from account.models.custom_user import CustomUser
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", "phone_number", "email", "first_name", "last_name",
            "is_active", "is_staff", "created_at", "updated_at", "password"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "password": {"write_only": True}
        }
    

    def validator_phone_number(value):
        if not value.startswith("+98"):
            raise serializers.ValidationError("Phone number must start with +98.")
        return value


    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
