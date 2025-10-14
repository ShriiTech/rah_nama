from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema_view

from account.schema.phone_token_schemas import PhoneTokenObtainSchema
from account.serializers.phone_token_obtain import PhoneTokenObtainSerializer


@extend_schema_view(
    post=PhoneTokenObtainSchema.post_schema
)
class PhoneTokenObtainView(APIView):
    permission_classes = []  # اجازه برای عموم (یا تنظیم دلخواه)
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = PhoneTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
