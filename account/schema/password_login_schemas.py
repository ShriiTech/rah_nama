from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from account.serializers import PasswordLoginSerializer


class PasswordLoginSchemas:
    """Schema برای API دریافت توکن با شماره موبایل"""

    post = extend_schema(
        summary="دریافت توکن با شماره موبایل",
        description="با ارسال شماره موبایل، توکن احراز هویت برای کاربر ایجاد و برگردانده می‌شود.",
        request=PasswordLoginSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=PasswordLoginSerializer,
                description="توکن با موفقیت ایجاد شد.",
                examples=[
                    OpenApiExample(
                        "موفق",
                        value={
                            "phone": "+989123456789",
                            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                        },
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="شماره موبایل نامعتبر یا فرمت اشتباه",
                examples=[
                    OpenApiExample(
                        "خطا",
                        value={"phone": ["این شماره موبایل معتبر نیست."]}
                    )
                ],
            ),
        },
    )
