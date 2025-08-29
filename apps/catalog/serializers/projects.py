
import logging
from rest_framework import serializers
from apps.catalog.models.projects import Project, Tag
from apps.catalog.models.medias import Media

logger = logging.getLogger(__name__)


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.
    
    Provides basic tag information for read operations.
    Used in project listings and details to show associated tags.
    """
    
    class Meta:
        model = Tag
        fields = ['id', 'name']


class MediaSerializer(serializers.ModelSerializer):
    """
    Serializer for Media model.
    
    Handles serialization of media files associated with projects.
    Includes file URL, caption, type, display order, and upload timestamp.
    Upload timestamp is read-only as it's automatically set.
    """
    
    class Meta:
        model = Media
        fields = ['id', 'file', 'caption', 'type', 'order', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer for project list view.
    
    Provides essential project information optimized for list display.
    Includes cover image URL and associated tags. Designed for performance
    in list views where detailed information is not needed.
    """
    
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
        """
        Generate absolute URL for project cover image.
        
        Constructs full URL including domain for the cover image
        if one exists. Returns None if no cover image is set.
        
        Args:
            obj: Project instance
            
        Returns:
            str or None: Absolute URL to cover image or None
        """
        try:
            if obj.cover and hasattr(obj.cover, 'url'):
                request = self.context.get('request')
                url = obj.cover.url
                absolute_url = request.build_absolute_uri(url) if request else url
                logger.debug(f"Generated cover URL for project {obj.id}: {absolute_url}")
                return absolute_url
            return None
        except Exception as e:
            logger.error(f"Error generating cover URL for project {obj.id}: {str(e)}")
            return None


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed project view.
    
    Provides complete project information including all fields,
    associated tags, and media files. Used for individual project
    display and API responses after create/update operations.
    
    Owner, creation, and modification timestamps are read-only.
    """
    
    tags = TagSerializer(many=True, read_only=True)
    media = MediaSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']


class ProjectWriteSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating projects.
    
    Handles project creation and updates with tag association.
    Uses tag_ids field for efficient tag assignment via primary keys.
    Owner is automatically set from request context during creation.
    
    Features:
    - Tag association via primary key relationships
    - Automatic slug generation (read-only)
    - Owner assignment from authenticated user
    - Support for both full and partial updates
    """
    
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
        read_only_fields = ['slug']

    def create(self, validated_data):
        """
        Create a new project instance.
        
        Extracts tag IDs from validated data and creates project
        with the authenticated user as owner. Associates tags
        after project creation.
        
        Args:
            validated_data: Validated serializer data
            
        Returns:
            Project: Created project instance
            
        Raises:
            ValidationError: If required data is missing or invalid
        """
        try:
            # Note: Fixed the typo in the original code ('tags' -> None)
            tag_ids = validated_data.pop('tag_ids', None)
            
            user = self.context['request'].user
            logger.info(f"Creating project '{validated_data.get('title')}' for user {user}")
            
            project = Project.objects.create(owner=user, **validated_data)
            
            if tag_ids:
                project.tags.set(tag_ids)
                logger.debug(f"Associated {len(tag_ids)} tags with project {project.id}")
            
            logger.info(f"Project created successfully with ID: {project.id}")
            return project
            
        except Exception as e:
            logger.error(f"Error creating project: {str(e)}", exc_info=True)
            raise

    def update(self, instance, validated_data):
        """
        Update an existing project instance.
        
        Updates project fields and manages tag associations.
        If tag_ids is provided, replaces all existing tag associations.
        If tag_ids is None, leaves existing tags unchanged.
        
        Args:
            instance: Project instance to update
            validated_data: Validated serializer data
            
        Returns:
            Project: Updated project instance
            
        Raises:
            ValidationError: If update data is invalid
        """
        try:
            tag_ids = validated_data.pop('tag_ids', None)
            
            logger.info(f"Updating project {instance.id} - {instance.title}")
            logger.debug(f"Update fields: {list(validated_data.keys())}")
            
            instance = super().update(instance, validated_data)
            
            if tag_ids is not None:
                instance.tags.set(tag_ids)
                logger.debug(f"Updated tags for project {instance.id}: {len(tag_ids)} tags")
            
            logger.info(f"Project {instance.id} updated successfully")
            return instance
            
        except Exception as e:
            logger.error(f"Error updating project {instance.id}: {str(e)}", exc_info=True)
            raise