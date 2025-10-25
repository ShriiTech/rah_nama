import logging
from django.core.cache import cache
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema_view


from account.schema.update.email import RequestEmailUpdateSchema
from account.serializers.update.email.request_email_update_serializers import RequestEmailUpdateSerializer
from utility.otp_code import OTPService


logger = logging.getLogger(__name__)

otp_service = OTPService()

@extend_schema_view(
    post=RequestEmailUpdateSchema.post()
)
class RequestEmailChangeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RequestEmailUpdateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = request.user
        new_email = serializer.validated_data["new_email"]
        redis_key = f"email_otp:{user.id}:{new_email}"

        # Check OTP resend cooldown
        if cache.get(redis_key):
            logger.info(f"User {user.id} tried to request OTP for {new_email} but OTP is still valid.")
            return Response(
                {"detail": "A verification code was already sent. Please wait before retrying."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
 
        # Generate and cache OTP
        otp_code = otp_service.generate_and_cache_otp(user.phone_number)

        logger.info(f"OTP code ({otp_code}) generated for user {user.id} to change email to {new_email}")

        send_mail(
            subject="Email change verification code",
            message=f"Your verification code is: {otp_code}",
            from_email="rah.nama.drf@gmail.com",
            recipient_list=[new_email],
        )
        logger.info(f"Verification email sent to {new_email} for user {user.id}")
        
        return Response(
            {"detail": "Verification code sent to new email."},
            status=status.HTTP_200_OK,
        )
