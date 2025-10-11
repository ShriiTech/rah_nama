from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from catalog.serializers.projects import ProjectListSerializer, ProjectDetailSerializer, ProjectWriteSerializer

class ProjectListCreateSchema:
    """Schema برای API لیست و ایجاد پروژه"""

    list_schema = extend_schema(
        summary="لیست پروژه‌ها",
        description="دریافت لیست همه پروژه‌ها با اطلاعات پایه و بهینه‌سازی کوئری‌ها",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=ProjectListSerializer(many=True),
                description="لیست پروژه‌ها با موفقیت دریافت شد",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="خطا در دریافت لیست پروژه‌ها",
            ),
        },
    )

    create_schema = extend_schema(
        summary="ایجاد پروژه جدید",
        description="ایجاد یک پروژه جدید توسط کاربر احراز هویت شده",
        request=ProjectWriteSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=ProjectDetailSerializer,
                description="پروژه با موفقیت ایجاد شد",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="خطا در داده‌های ورودی",
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
                description="خطای سرور در ایجاد پروژه",
            ),
        },
    )


class ProjectDetailSchema:
    """Schema برای API جزئیات، ویرایش و حذف پروژه"""

    retrieve_schema = extend_schema(
        summary="جزئیات پروژه",
        description="دریافت جزئیات یک پروژه بر اساس شناسه",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=ProjectDetailSerializer,
                description="جزئیات پروژه با موفقیت دریافت شد",
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="پروژه یافت نشد"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(description="خطای سرور"),
        },
    )

    update_schema = extend_schema(
        summary="ویرایش پروژه",
        description="ویرایش کامل یا جزئی پروژه توسط صاحب پروژه",
        request=ProjectWriteSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=ProjectDetailSerializer,
                description="پروژه با موفقیت ویرایش شد",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="خطا در داده‌های ورودی"),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="دسترسی غیرمجاز"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="پروژه یافت نشد"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(description="خطای سرور"),
        },
    )

    delete_schema = extend_schema(
        summary="حذف پروژه",
        description="حذف یک پروژه توسط صاحب پروژه",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="پروژه با موفقیت حذف شد"),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(description="دسترسی غیرمجاز"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="پروژه یافت نشد"),
            status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(description="خطای سرور"),
        },
    )
