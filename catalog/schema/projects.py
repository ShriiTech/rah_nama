from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
    OpenApiParameter,
)
from drf_spectacular.types import OpenApiTypes
from rest_framework import status

from catalog.serializers.projects import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectWriteSerializer,
)


# ------------------------------------------------------------------------
# 🔹 Project List & Create Schema
# ------------------------------------------------------------------------
class ProjectListCreateSchema:
    """📘 Schema برای API لیست و ایجاد پروژه‌ها"""

    list_schema = extend_schema(
        summary="لیست پروژه‌ها",
        description=(
            "دریافت لیست پروژه‌ها با پشتیبانی از فیلتر، جستجو و مرتب‌سازی.\n\n"
            "پارامترهای پشتیبانی‌شده:\n"
            "- `status`: فیلتر بر اساس وضعیت پروژه (مثلاً active, draft, completed)\n"
            "- `featured`: فیلتر پروژه‌های ویژه (true/false)\n"
            "- `search`: جستجو در عنوان، نام مالک، شماره پرونده و آدرس\n"
            "- `ordering`: مرتب‌سازی بر اساس هر فیلد (مثلاً `-created_at`, `title`)"
        ),
        parameters=[
            OpenApiParameter(
                name="status",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="فیلتر بر اساس وضعیت پروژه",
            ),
            OpenApiParameter(
                name="featured",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="نمایش فقط پروژه‌های ویژه (true/false)",
            ),
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="جستجو در عنوان، شماره پرونده، نام مالک یا آدرس پروژه",
            ),
            OpenApiParameter(
                name="ordering",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="مرتب‌سازی پروژه‌ها (مثلاً `-created_at` یا `title`)",
            ),
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=ProjectListSerializer(many=True),
                description="✅ لیست پروژه‌ها با موفقیت دریافت شد",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="❌ خطا در دریافت لیست پروژه‌ها",
            ),
        },
        examples=[
            OpenApiExample(
                "نمونه خروجی",
                value=[
                    {
                        "id": 1,
                        "title": "ساخت برج اداری",
                        "slug": "office-tower",
                        "municipal_file_number": "MUN-1403-01",
                        "owner_name": "علی احمدی",
                        "status": "ongoing",
                        "featured": True,
                        "cover": "/media/projects/cover1.jpg",
                        "created_at": "2025-01-01T08:00:00Z",
                    }
                ],
            )
        ],
    )

    create_schema = extend_schema(
        summary="ایجاد پروژه جدید",
        description="ایجاد یک پروژه جدید توسط کاربر احراز هویت‌شده.",
        request=ProjectWriteSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=ProjectDetailSerializer,
                description="✅ پروژه با موفقیت ایجاد شد",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="❌ داده‌های ارسالی نامعتبر است",
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                description="❌ نیاز به ورود کاربر دارد",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="❌ خطا در فرآیند ایجاد پروژه",
            ),
        },
        examples=[
            OpenApiExample(
                "نمونه درخواست ایجاد پروژه",
                value={
                    "title": "بازسازی کتابخانه مرکزی",
                    "summary": "پروژه بازسازی و توسعه ساختمان کتابخانه",
                    "location": "خیابان انقلاب، تهران",
                    "area_sqm": 1500,
                    "budget": 2500000000,
                    "status": "planning",
                    "featured": False,
                    "tags": [1, 3],
                },
            )
        ],
    )


# ------------------------------------------------------------------------
# 🔹 Project Detail Schema
# ------------------------------------------------------------------------
class ProjectDetailSchema:
    """📗 Schema برای جزئیات، ویرایش و حذف پروژه"""

    retrieve_schema = extend_schema(
        summary="دریافت جزئیات پروژه",
        description="دریافت اطلاعات کامل پروژه بر اساس شناسه یا slug.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=ProjectDetailSerializer,
                description="✅ جزئیات پروژه با موفقیت دریافت شد",
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="❌ پروژه یافت نشد",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="❌ خطا در واکشی اطلاعات پروژه",
            ),
        },
        examples=[
            OpenApiExample(
                "نمونه خروجی",
                value={
                    "id": 2,
                    "title": "مرکز خرید جدید",
                    "slug": "shopping-center",
                    "summary": "ساخت یک مرکز خرید بزرگ در منطقه شمالی",
                    "owner_name": "شرکت عمران توسعه",
                    "status": "active",
                    "featured": False,
                    "address": "بلوار کاوه، اصفهان",
                    "start_date": "2025-02-01",
                    "end_date": "2026-12-30",
                    "tags": [{"id": 3, "name": "تجاری", "slug": "commercial"}],
                    "created_at": "2025-02-10T14:30:00Z",
                    "updated_at": "2025-03-12T10:00:00Z",
                },
            )
        ],
    )

    update_schema = extend_schema(
        summary="ویرایش پروژه",
        description="ویرایش کامل (PUT) یا جزئی (PATCH) یک پروژه توسط مالک.",
        request=ProjectWriteSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=ProjectDetailSerializer,
                description="✅ پروژه با موفقیت ویرایش شد",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="❌ داده‌های ارسالی نامعتبر است",
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="❌ کاربر مجاز به ویرایش این پروژه نیست",
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="❌ پروژه یافت نشد",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="❌ خطای سرور در ویرایش پروژه",
            ),
        },
        examples=[
            OpenApiExample(
                "نمونه ویرایش جزئی پروژه",
                value={
                    "title": "مرکز خرید بزرگ اصفهان",
                    "budget": 3800000000,
                    "featured": True,
                    "tags": [1, 5],
                },
            )
        ],
    )

    delete_schema = extend_schema(
        summary="حذف پروژه",
        description="حذف پروژه توسط مالک. در صورت موفقیت، هیچ پاسخی بازگردانده نمی‌شود.",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="✅ پروژه با موفقیت حذف شد"
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="❌ کاربر مجاز به حذف این پروژه نیست"
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="❌ پروژه یافت نشد"
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="❌ خطا در فرآیند حذف پروژه"
            ),
        },
    )
