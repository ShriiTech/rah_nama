from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema_view

from account.schema import PasswordLoginSchemas
from account.serializers import PasswordLoginSerializer


@extend_schema_view(
    post=PasswordLoginSchemas.post
)
class PasswordLoginAPIView(APIView):
    permission_classes = []  
    authentication_classes = []
    serializer_class = PasswordLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
