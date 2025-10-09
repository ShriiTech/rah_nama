from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


class CustomTokenRefreshSerializer(serializers.Serializer):
    """
    Custom serializer for refreshing JWT tokens.
    Validates the refresh token and returns a new access token.
    """

    refresh = serializers.CharField(
        required=True,
        help_text="The refresh token to be used for obtaining a new access token.",
        style={"input_type": "textarea"},
    )

    access = serializers.CharField(read_only=True, help_text="Newly generated access token.")
    refresh_new = serializers.CharField(
        read_only=True,
        help_text="Newly generated refresh token (if rotation is enabled)."
    )

    def validate_refresh(self, value):
        """Ensure refresh token is not empty and is a valid format."""
        if not value or len(value) < 20:
            raise serializers.ValidationError("Refresh token is invalid or malformed.")
        return value

    def validate(self, attrs):
        """
        Validate the refresh token and generate a new access token.
        Uses SimpleJWT's built-in TokenRefreshSerializer internally.
        """
        token_data = {"refresh": attrs.get("refresh")}
        simplejwt_serializer = TokenRefreshSerializer(data=token_data)

        try:
            simplejwt_serializer.is_valid(raise_exception=True)
        except TokenError:
            raise serializers.ValidationError({
                "refresh": "Invalid or expired refresh token."
            })

        validated_data = simplejwt_serializer.validated_data
        return {
            "access": validated_data.get("access"),
            "refresh_new": validated_data.get("refresh")
        }
