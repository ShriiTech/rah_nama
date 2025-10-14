from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from drf_spectacular.utils import extend_schema_view

from account.schema.update.password.update_password_sckemas import ChangePasswordSchema
from account.serializers.update.password.update_password_serializers import ChangePasswordSerializer


@extend_schema_view(
    post=ChangePasswordSchema.post_schema
)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # بعد از تغییر پسورد، تمام توکن‌های این کاربر رو blacklist کن
        self._logout_all_tokens(user)

        return Response(
            {"detail": "Password changed successfully. All active tokens have been invalidated."},
            status=status.HTTP_200_OK
        )

    def _logout_all_tokens(self, user):
        """تمام توکن‌های این کاربر رو blacklist کن"""
        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            try:
                BlacklistedToken.objects.get_or_create(token=token)
            except Exception:
                pass
