from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter

from rest_framework import status

from catalog.serializers.medias import MediaSerializer


class ProjectMediaUploadSchema:
    """Schema برای API آپلود چند فایل در پروژه"""

    post_schema = extend_schema(
        summary="آپلود چند فایل به پروژه",
        description="فایل‌های ارسالی به پروژه اضافه می‌شوند. فقط صاحب پروژه می‌تواند آپلود کند.",
        request=None,  # فایل‌ها معمولا با form-data ارسال می‌شوند، می‌توان از OpenApiParameter برای توضیح استفاده کرد
        parameters=[
            OpenApiParameter(
                name='files',
                description='چند فایل برای آپلود (type=file)',
                required=True,
                type='file',
                many=True
            ),
            OpenApiParameter(
                name='pk',
                description='شناسه پروژه',
                required=True,
                type=int
            ),
        ],
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=MediaSerializer(many=True),
                description="فایل‌ها با موفقیت آپلود شدند.",
                examples=[
                    OpenApiExample(
                        "موفق",
                        value=[
                            {
                                "id": 1,
                                "project": 1,
                                "file": "http://example.com/media/image1.jpg",
                                "type": "image"
                            },
                            {
                                "id": 2,
                                "project": 1,
                                "file": "http://example.com/media/image2.jpg",
                                "type": "image"
                            }
                        ]
                    )
                ]
            ),
            status.HTTP_403_FORBIDDEN: OpenApiResponse(
                description="کاربر اجازه آپلود ندارد",
                examples=[OpenApiExample("خطا", value={"detail": "Not allowed"})]
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="پروژه یافت نشد",
                examples=[OpenApiExample("خطا", value={"detail": "Not Found"})]
            ),
        },
    )
