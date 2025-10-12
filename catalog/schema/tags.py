from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import status
from catalog.serializers.projects import TagSerializer


class TagListCreateSchema:
    """Schema برای API لیست و ایجاد Tag"""

    list_schema = extend_schema(
        summary="لیست تمام Tagها",
        description="دریافت لیست همه Tagها",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TagSerializer(many=True),
                description="لیست Tagها با موفقیت دریافت شد",
            ),
        },
    )

    create_schema = extend_schema(
        summary="ایجاد Tag جدید",
        description="ایجاد یک Tag جدید",
        request=TagSerializer,
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=TagSerializer,
                description="Tag با موفقیت ایجاد شد",
                examples=[
                    OpenApiExample(
                        "موفق",
                        value={
                            "id": 1,
                            "name": "Django",
                        },
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="خطا در داده‌های ورودی",
            ),
        },
    )


class TagDetailSchema:
    """Schema برای API جزئیات، ویرایش و حذف Tag"""

    retrieve_schema = extend_schema(
        summary="جزئیات Tag",
        description="دریافت جزئیات یک Tag بر اساس شناسه",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TagSerializer,
                description="جزئیات Tag با موفقیت دریافت شد",
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Tag یافت نشد"),
        },
    )

    update_schema = extend_schema(
        summary="ویرایش Tag",
        description="ویرایش یک Tag",
        request=TagSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=TagSerializer,
                description="Tag با موفقیت ویرایش شد",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(description="خطا در داده‌های ورودی"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Tag یافت نشد"),
        },
    )

    delete_schema = extend_schema(
        summary="حذف Tag",
        description="حذف یک Tag",
        responses={
            status.HTTP_204_NO_CONTENT: OpenApiResponse(description="Tag با موفقیت حذف شد"),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(description="Tag یافت نشد"),
        },
    )
