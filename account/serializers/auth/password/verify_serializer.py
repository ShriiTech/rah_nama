from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class TokenVerifySerializer(serializers.Serializer):
    """
    Custom serializer for verifying JWT tokens.
    Checks if the given token (access or refresh) is valid.
    """

    token = serializers.CharField(
        required=True,
        help_text="JWT access or refresh token to verify.",
        style={"input_type": "textarea"},
    )

    def validate_token(self, value):
        """
        Validate token structure before passing to SimpleJWT verification.
        """
        if not value or len(value) < 20:
            raise serializers.ValidationError("Token is invalid or malformed.")
        return value

    def validate(self, attrs):
        """
        Verify token using SimpleJWT built-in TokenVerifySerializer.
        """
        token_data = {"token": attrs.get("token")}
        simplejwt_serializer = TokenVerifySerializer(data=token_data)

        try:
            simplejwt_serializer.is_valid(raise_exception=True)
        except (TokenError, InvalidToken):
            raise serializers.ValidationError({
                "token": "Invalid or expired token."
            })

        return {"detail": "Token is valid."}
