from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class TokenRefreshAPIView(APIView):
    """
    Refresh JWT token using the provided refresh token.
    """

    permission_classes = [AllowAny]  # اجازه دسترسی عمومی برای رفرش توکن

    def post(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            return Response(
                {"detail": "Invalid or expired refresh token.", "error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
