from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema_view


from account.schema.update.email.update_verify_email_schemas import VerifyEmailChangeSchema
from account.serializers.update.email.verify_email_otp_serializers import VerifyEmailOTPSerializer


@extend_schema_view(
    post=VerifyEmailChangeSchema.post_schema
)
class VerifyEmailChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VerifyEmailOTPSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Email updated successfully."}, status=status.HTTP_200_OK)