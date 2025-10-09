from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from account.serializers.auth.password.verify_serializer import TokenVerifySerializer


class TokenVerifyAPIView(APIView):
    """
    API endpoint to verify JWT tokens (access or refresh).
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = TokenVerifySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
