from rest_framework import serializers
from catalog.models.medias import Media


class MediaSerializer(serializers.ModelSerializer):
    """
    Serializer for Media model.

    - Supports image, video, and file uploads.
    - Handles ordering and project relationship.
    """

    # Read-only field to display project title
    project_title = serializers.CharField(source='project.title', read_only=True)

    # uploaded_at should be read-only
    uploaded_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Media
        fields = [
            'id',
            'project',
            'project_title',
            'file',
            'caption',
            'type',
            'order',
            'uploaded_at',
        ]
        read_only_fields = ['id', 'project_title', 'uploaded_at']

    def validate_type(self, value):
        """Ensure the type matches the uploaded file format"""
        valid_types = [choice[0] for choice in self.Meta.model.FILE_TYPES]
        if value not in valid_types:
            raise serializers.ValidationError(f"Invalid type '{value}'. Valid types: {valid_types}")
        return value

    def validate(self, attrs):
        """
        Additional validation:
        - Ensure 'file' field matches 'type' if needed
        """
        file = attrs.get('file')
        media_type = attrs.get('type', 'image')

        if file:
            content_type = file.content_type.split('/')[0]  # e.g., 'image', 'video', 'application'
            if media_type == 'image' and content_type != 'image':
                raise serializers.ValidationError("Uploaded file is not an image")
            if media_type == 'video' and content_type != 'video':
                raise serializers.ValidationError("Uploaded file is not a video")
            if media_type == 'file' and content_type in ['image', 'video']:
                raise serializers.ValidationError("Uploaded file cannot be an image or video for type 'file'")
        return attrs
