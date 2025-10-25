from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from account.serializers.models.custom_user_serializers import CustomUserSerializer


class PersonalInfoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get(self, request):
        my_custom_user = request.user
        serializer = self.serializer_class(my_custom_user)
        return Response(serializer.data)
    