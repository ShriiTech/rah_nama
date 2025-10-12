# utility/otpcode/refresh_token_api.py
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.exceptions import InvalidToken

from rest_framework.permissions import AllowAny


logger = logging.getLogger(__name__)


class RefreshTokenAPIView(APIView):
    """
    POST: { "refresh": "<refresh_token>" }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh", "").strip()
        if not refresh_token:
            logger.warning("Refresh token not provided")
            return Response({"detail": "Refresh token ارسال نشده است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            new_access = str(refresh.access_token)
            logger.info("Access token refreshed successfully")
            return Response({"access": new_access}, status=status.HTTP_200_OK)
        except TokenError as e:
            logger.warning(f"Invalid refresh token: {e}")
            return Response({"detail": "Refresh token نامعتبر است."}, status=status.HTTP_401_UNAUTHORIZED)
