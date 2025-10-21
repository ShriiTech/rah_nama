from rest_framework import serializers
from catalog.models import Project
from catalog.models.tags import Tag


# ------------------------------------------------------------------------
# 🔹 Tag Serializer (برای نمایش ساده‌ی تگ‌ها داخل پروژه)
# ------------------------------------------------------------------------
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]
        read_only_fields = ["id", "slug"]


# ------------------------------------------------------------------------
# 🔹 Project List Serializer
# فقط فیلدهایی که در لیست نیاز داریم (برای performance)
# ------------------------------------------------------------------------
class ProjectListSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.get_full_name", read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "municipal_file_number",
            "owner_name",
            "status",
            "featured",
            "cover",
            "created_at",
            "tags",
        ]
        read_only_fields = ["slug"]


# ------------------------------------------------------------------------
# 🔹 Project Detail Serializer
# برای نمایش جزئیات کامل پروژه
# ------------------------------------------------------------------------
class ProjectDetailSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.get_full_name", read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "slug",
            "summary",
            "location",
            "area_sqm",
            "budget",
            "municipal_file_number",
            "owner",
            "owner_name",
            "total_area",
            "floors_count",
            "start_date",
            "end_date",
            "address",
            "status",
            "featured",
            "cover",
            "tags",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "owner",
            "created_at",
            "updated_at",
        ]


# ------------------------------------------------------------------------
# 🔹 Project Write Serializer
# برای ساخت و ویرایش پروژه‌ها (Create / Update)
# ------------------------------------------------------------------------
class ProjectWriteSerializer(serializers.ModelSerializer):
    """
    Write serializer — used for create/update operations.
    Includes validation and allows setting tags.
    """

    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(), required=False
    )

    class Meta:
        model = Project
        fields = [
            "title",
            "summary",
            "location",
            "area_sqm",
            "budget",
            "municipal_file_number",
            "owner_name",
            "total_area",
            "floors_count",
            "start_date",
            "end_date",
            "address",
            "status",
            "featured",
            "cover",
            "tags",
        ]

    def validate_budget(self, value):
        """Ensure budget is non-negative."""
        if value is not None and value < 0:
            raise serializers.ValidationError("Budget cannot be negative.")
        return value

    def validate(self, data):
        """Ensure start_date is before end_date."""
        start = data.get("start_date")
        end = data.get("end_date")
        if start and end and start > end:
            raise serializers.ValidationError(
                {"end_date": "End date must be after start date."}
            )
        return data

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        project = Project.objects.create(**validated_data)
        if tags:
            project.tags.set(tags)
        return project

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            instance.tags.set(tags)
        return instance
