from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status


class TestAuthAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        customuser = request.user
        if customuser.is_anonymous:
            return Response({"detail": "کاربر احراز هویت نشده است ❌"}, status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            return Response({
                "message": "احراز هویت با موفقیت انجام شد ✅",
                "user": {
                    "id": customuser.id,
                    "phone_number": customuser.phone_number,
                    "first_name": customuser.first_name,
                    "last_name": customuser.last_name,
                }
            }, status=status.HTTP_200_OK)
        
