from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view
from django.contrib.auth import get_user_model


from account.schema.update.email.verify import VerifyEmailUpdateSchema
from account.serializers.update.email.verify_email_update_serializers import VerifyEmailUpdateSerializer
from utility.otp_code import OTPService


User = get_user_model()
otp_service = OTPService()


@extend_schema_view(
    post=VerifyEmailUpdateSchema.post()
)
class VerifyEmailChangeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VerifyEmailUpdateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        new_email = serializer.validated_data["new_email"]
        user = request.user

        # --- Business logic here ---
        user.email = new_email
        user.save(update_fields=["email"])
        otp_service.invalidate_otp(user.phone_number)

        return Response({"detail": "Email updated successfully."}, status=status.HTTP_200_OK)
