from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from account.serializers.custom_user import CustomUserSerializer


class MyCustomUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        my_custom_user = request.user
        serializer = CustomUserSerializer(my_custom_user)
        return Response(serializer.data)
    