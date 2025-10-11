from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
)
from rest_framework import status
from account.serializers.custom_user import CustomUserSerializer


class CustomUserListCreateSchema:
    """مستندات مربوط به API لیست و ایجاد کاربر جدید"""

    list_schema = extend_schema(
        summary="لیست کاربران",
        description="دریافت لیست تمام کاربران ثبت‌شده (فقط برای ادمین‌ها).",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=CustomUserSerializer(many=True),
                description="لیست کاربران با موفقیت دریافت شد.",
                examples=[
                    OpenApiExample(
                        "موفق",
                        value=[
                            {
                                "id": 1,
                                "username": "admin",
                                "email": "admin@example.com",
                                "first_name": "ادمین",
                                "last_name": "سیستم",
                            },
                            {
                                "id": 2,
                                "username": "user1",
                                "email": "user1@example.com",
                                "first_name": "علی",
                                "last_name": "رضایی",
                            },
                        ],
                    )
                ],
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="دسترسی غیرمجاز (فقط ادمین‌ها مجاز هستند)"
            ),
        },
    )

    create_schema = extend_schema(
        summary="ایجاد کاربر جدید",
        description="افزودن یک کاربر جدید با اطلاعات ورودی.",
        request=CustomUserSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=CustomUserSerializer,
                description="کاربر جدید با موفقیت ایجاد شد.",
                examples=[
                    OpenApiExample(
                        "نمونه موفق",
                        value={
                            "id": 3,
                            "username": "new_user",
                            "email": "new_user@example.com",
                            "first_name": "نیلوفر",
                            "last_name": "موسوی",
                        },
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="ورودی نامعتبر",
                examples=[
                    OpenApiExample("خطا", value={"email": ["This field must be unique."]}),
                ],
            ),
        },
    )


class CustomUserDetailSchema:
    """مستندات مربوط به API جزئیات، ویرایش و حذف کاربر"""

    retrieve_schema = extend_schema(
        summary="دریافت جزئیات کاربر",
        description="دریافت اطلاعات کاربر بر اساس شناسه (pk).",
        parameters=[
            OpenApiParameter("pk", description="شناسه کاربر", required=True, type=int),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=CustomUserSerializer,
                description="اطلاعات کاربر با موفقیت برگردانده شد.",
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="کاربر یافت نشد",
                examples=[OpenApiExample("کاربر یافت نشد", value={"detail": "User not found"})],
            ),
        },
    )

    update_schema = extend_schema(
        summary="ویرایش جزئی اطلاعات کاربر",
        description="ویرایش بخشی از اطلاعات کاربر با شناسه مشخص‌شده.",
        request=CustomUserSerializer,
        parameters=[
            OpenApiParameter("pk", description="شناسه کاربر", required=True, type=int),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=CustomUserSerializer,
                description="کاربر با موفقیت به‌روزرسانی شد.",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="داده‌های نامعتبر",
                examples=[
                    OpenApiExample("خطا", value={"email": ["فرمت ایمیل اشتباه است."]}),
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="کاربر یافت نشد",
                examples=[OpenApiExample("کاربر یافت نشد", value={"detail": "User not found"})],
            ),
        },
    )

    delete_schema = extend_schema(
        summary="حذف کاربر",
        description="حذف کاربر با شناسه مشخص‌شده.",
        parameters=[
            OpenApiParameter("pk", description="شناسه کاربر", required=True, type=int),
        ],
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="کاربر با موفقیت حذف شد."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="کاربر یافت نشد",
                examples=[OpenApiExample("کاربر یافت نشد", value={"detail": "User not found"})],
            ),
        },
    )
