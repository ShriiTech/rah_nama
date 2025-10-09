from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import logging

logger = logging.getLogger(__name__)

class TokenRefreshAPIView(APIView):
    """
    Custom APIView for refreshing JWT tokens.
    Uses DRF SimpleJWT's TokenRefreshSerializer under the hood.
    """

    permission_classes = [AllowAny]  # Anyone can hit this endpoint with a refresh token

    def post(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            logger.warning(
                "Invalid refresh attempt",
                extra={
                    "ip": self.get_client_ip(request),
                    "user_agent": request.META.get("HTTP_USER_AGENT", ""),
                    "error": str(e),
                },
            )
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            logger.error("Unexpected error during refresh", exc_info=True)
            return Response(
                {"detail": "Something went wrong."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Optionally: rotate refresh tokens (depends on SIMPLE_JWT settings)
        data = serializer.validated_data
        return Response(
            {
                "access": data.get("access"),
                "refresh": data.get("refresh"),  # if ROTATE_REFRESH_TOKENS=True
            },
            status=status.HTTP_200_OK,
        )

    def get_client_ip(self, request):
        """Helper to extract client IP (works with reverse proxy too)."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")
