from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from account.serializers.phone_token_obtain import PhoneTokenObtainSerializer


class PhoneTokenObtainView(APIView):
    permission_classes = []  # اجازه برای عموم (یا تنظیم دلخواه)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = PhoneTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
