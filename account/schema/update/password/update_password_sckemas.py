from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from rest_framework import status
from account.serializers.update.password.update_password_serializers import ChangePasswordSerializer


class ChangePasswordSchema:
    """مستندات مربوط به API تغییر پسورد"""

    post_schema = extend_schema(
        summary="تغییر پسورد کاربر",
        description=(
            "این API برای کاربران احراز هویت شده اجازه می‌دهد تا پسورد خود را تغییر دهند. "
            "پس از تغییر پسورد، تمام توکن‌های فعال این کاربر باطل می‌شوند."
        ),
        request=ChangePasswordSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="پسورد با موفقیت تغییر کرد و توکن‌های فعال باطل شدند.",
                response={
                    "type": "object",
                    "properties": {
                        "detail": {
                            "type": "string",
                            "example": "Password changed successfully. All active tokens have been invalidated."
                        }
                    },
                },
                examples=[
                    OpenApiExample(
                        "تغییر موفق پسورد",
                        summary="مثال موفقیت‌آمیز",
                        value={
                            "detail": "Password changed successfully. All active tokens have been invalidated."
                        },
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="ورودی نامعتبر یا پسورد جدید با قوانین مطابقت ندارد",
                examples=[
                    OpenApiExample(
                        "خطای ورودی",
                        summary="مثال خطا",
                        value={"new_password": ["This password is too weak."]},
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
        },
    )
