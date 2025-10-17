from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema_view

from account.schema.update.email.update_emai_schemas import RequestEmailChangeSchema
from account.serializers.update.email.update_email_serializer import RequestEmailChangeSerializer


@extend_schema_view(
    post=RequestEmailChangeSchema.post_schema
)
class RequestEmailChangeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestEmailChangeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Verification code sent to new email."}, status=status.HTTP_200_OK)



