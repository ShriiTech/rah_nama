from rest_framework import serializers
from apps.catalog.models.projects import Project, Tag
from apps.catalog.models.media import Media


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'file', 'caption', 'type', 'order', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class ProjectListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'summary', 'location',
            'area_sqm', 'status', 'featured',
            'cover_url', 'tags', 'created_at'
        ]

    def get_cover_url(self, obj):
        if obj.cover and hasattr(obj.cover, 'url'):
            request = self.context.get('request')
            url = obj.cover.url
            return request.build_absolute_uri(url) if request else url
        return None


class ProjectDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']


class ProjectWriteSerializer(serializers.ModelSerializer):
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Project
        fields = [
            'title', 'slug', 'summary', 'location', 'area_sqm',
            'budget', 'start_date', 'end_date',
            'status', 'featured', 'cover', 'tag_ids'
        ]

    def create(self, validated_data):
        tag_ids = validated_data.pop('tag_ids','tags')
        project = Project.objects.create(owner=self.context['request'].user, **validated_data)
        if tag_ids:
            project.tags.set(tag_ids)
        return project

    def update(self, instance, validated_data):
        tag_ids = validated_data.pop('tag_ids', None)
        instance = super().update(instance, validated_data)
        if tag_ids is not None:
            instance.tags.set(tag_ids)
        return instance
