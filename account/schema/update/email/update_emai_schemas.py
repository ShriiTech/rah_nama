from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
)
from rest_framework import status
from account.serializers.update.email.update_email_serializer import RequestEmailChangeSerializer


class RequestEmailChangeSchema:
    """مستندات مربوط به API درخواست تغییر ایمیل"""

    post_schema = extend_schema(
        summary="درخواست تغییر ایمیل",
        description=(
            "این API برای کاربران احراز هویت شده اجازه می‌دهد تا ایمیل خود را تغییر دهند. "
            "کد تایید به ایمیل جدید ارسال می‌شود و تا تایید، ایمیل قدیمی معتبر باقی می‌ماند."
        ),
        request=RequestEmailChangeSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                description="کد تایید با موفقیت به ایمیل جدید ارسال شد.",
                response={
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Verification code sent to new email."
                        }
                    },
                },
                examples=[
                    OpenApiExample(
                        "درخواست موفق",
                        summary="مثال موفقیت‌آمیز",
                        value={"detail": "Verification code sent to new email."},
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="ورودی نامعتبر یا فرمت ایمیل اشتباه",
                examples=[
                    OpenApiExample(
                        "خطای ورودی",
                        summary="فرمت ایمیل اشتباه",
                        value={"new_email": ["Invalid email format."]},
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
            status.HTTP_409_CONFLICT: OpenApiResponse(
                description="ایمیل وارد شده قبلاً ثبت شده است",
                examples=[
                    OpenApiExample(
                        "ایمیل تکراری",
                        summary="Conflict example",
                        value={"detail": "Email already in use."},
                    )
                ],
            ),
        },
    )
