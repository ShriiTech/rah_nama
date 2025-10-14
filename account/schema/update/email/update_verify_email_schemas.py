from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework import status
from account.serializers.update.email.verify_email_otp_serializers import VerifyEmailOTPSerializer


class VerifyEmailChangeSchema:
    """مستندات مربوط به API تایید تغییر ایمیل با OTP"""

    post_schema = extend_schema(
        summary="تایید تغییر ایمیل",
        description=(
            "این API برای تایید تغییر ایمیل کاربر استفاده می‌شود. "
            "کاربر باید کد OTP دریافتی در ایمیل جدید را ارسال کند تا ایمیل به‌روزرسانی شود."
        ),
        request=VerifyEmailOTPSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="ایمیل با موفقیت به‌روزرسانی شد.",
                response={
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Email updated successfully."
                        }
                    },
                },
                examples=[
                    OpenApiExample(
                        "تایید موفق",
                        summary="مثال موفقیت‌آمیز",
                        value={"detail": "Email updated successfully."},
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="OTP نامعتبر یا ورودی اشتباه",
                examples=[
                    OpenApiExample(
                        "OTP اشتباه",
                        summary="مثال خطا",
                        value={"otp_code": ["Invalid OTP code."]},
                    )
                ],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="کاربر احراز هویت نشده است",
                examples=[
                    OpenApiExample(
                        "عدم احراز هویت",
                        summary="کاربر login نکرده",
                        value={"detail": "Authentication credentials were not provided."},
                    )
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="ایمیل جدید برای تایید پیدا نشد یا منقضی شده",
                examples=[
                    OpenApiExample(
                        "ایمیل یافت نشد",
                        summary="مثال خطا",
                        value={"detail": "Email change request not found."},
                    )
                ],
            ),
        },
    )
