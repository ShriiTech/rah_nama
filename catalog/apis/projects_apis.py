import logging

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from catalog.models import Project
from catalog.serializers.projects import (
    ProjectListSerializer, ProjectDetailSerializer, ProjectWriteSerializer,
)

logger = logging.getLogger(__name__)


class ProjectListCreateAPIView(APIView):
    """
    API View for listing all projects and creating new projects.
    
    Provides:
    - GET: Returns a paginated list of all projects with basic information
    - POST: Creates a new project (authentication required via serializer)
    
    Permissions:
    - GET: Allow any user (anonymous access)
    - POST: Handled by serializer validation
    """
    
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """
        Retrieve all projects with optimized database queries.
        
        Returns a list of projects with their basic information including
        owner details, tags, and media through select_related and 
        prefetch_related for optimal performance.
        
        Args:
            request: HTTP request object
            
        Returns:
            Response: JSON response containing list of projects
            
        Raises:
            DatabaseError: If database query fails
        """
        try:
            logger.info("Fetching all projects for listing")
            projects = Project.objects.all().select_related('owner').prefetch_related('tags', 'media')
            logger.debug(f"Retrieved {projects.count()} projects from database")
            
            serializer = ProjectListSerializer(projects, many=True, context={'request': request})
            
            logger.info(f"Successfully serialized {len(serializer.data)} projects")
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error fetching projects: {str(e)}", exc_info=True)
            return Response(
                {'detail': 'An error occurred while fetching projects'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """
        Create a new project.
        
        Validates the request data and creates a new project instance.
        The project owner is automatically set to the requesting user.
        
        Args:
            request: HTTP request object containing project data
            
        Returns:
            Response: JSON response with created project details or validation errors
            
        Status Codes:
            201: Project created successfully
            400: Invalid data provided
            500: Server error during creation
        """
        try:
            logger.info(f"Creating new project for user: {request.user}")
            logger.debug(f"Project data received: {request.data}")
            
            serializer = ProjectWriteSerializer(data=request.data, context={'request': request})
            
            if serializer.is_valid():
                project = serializer.save()
                logger.info(f"Project created successfully with ID: {project.id}")
                
                response_serializer = ProjectDetailSerializer(project, context={'request': request})
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.warning(f"Project creation failed - validation errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Error creating project: {str(e)}", exc_info=True)
            return Response(
                {'detail': 'An error occurred while creating the project'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ProjectDetailAPIView(APIView):
    """
    API View for retrieving, updating, and deleting individual projects.
    
    Provides:
    - GET: Returns detailed project information (public access)
    - PUT: Full update of project (owner only)
    - PATCH: Partial update of project (owner only)  
    - DELETE: Delete project (owner only)
    
    Permissions:
    - GET: Any user (authenticated or anonymous)
    - PUT/PATCH/DELETE: Owner only
    """
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        """
        Retrieve a project instance by primary key with optimized queries.
        
        Uses prefetch_related to minimize database queries for related
        tags and media objects.
        
        Args:
            pk: Primary key of the project
            
        Returns:
            Project: Project instance
            
        Raises:
            Http404: If project with given pk does not exist
        """
        logger.debug(f"Fetching project with ID: {pk}")
        try:
            project = get_object_or_404(Project.objects.prefetch_related('tags', 'media'), pk=pk)
            logger.debug(f"Successfully retrieved project: {project.title}")
            return project
        except Exception as e:
            logger.error(f"Error retrieving project {pk}: {str(e)}")
            raise

    def get(self, request, pk):
        """
        Retrieve detailed information for a specific project.
        
        Args:
            request: HTTP request object
            pk: Primary key of the project
            
        Returns:
            Response: JSON response with detailed project information
            
        Status Codes:
            200: Project retrieved successfully
            404: Project not found
            500: Server error during retrieval
        """
        try:
            logger.info(f"Retrieving project details for ID: {pk}")
            project = self.get_object(pk)
            
            serializer = ProjectDetailSerializer(project, context={'request': request})
            logger.info(f"Successfully retrieved project details: {project.title}")
            
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error retrieving project {pk}: {str(e)}", exc_info=True)
            return Response(
                {'detail': 'An error occurred while retrieving the project'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk):
        """
        Perform full update of a project (replace all fields).
        
        Only the project owner can update the project. All fields
        are replaced with new values (partial=False).
        
        Args:
            request: HTTP request object containing updated project data
            pk: Primary key of the project to update
            
        Returns:
            Response: JSON response with updated project or errors
            
        Status Codes:
            200: Project updated successfully
            400: Invalid data provided
            403: User is not the project owner
            404: Project not found
            500: Server error during update
        """
        try:
            logger.info(f"Full update requested for project {pk} by user {request.user}")
            project = self.get_object(pk)
            
            # Check ownership
            if project.owner != request.user:
                logger.warning(f"Unauthorized update attempt on project {pk} by user {request.user}")
                return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)

            logger.debug(f"Update data for project {pk}: {request.data}")
            serializer = ProjectWriteSerializer(
                project, 
                data=request.data, 
                partial=False, 
                context={'request': request}
            )
            
            if serializer.is_valid():
                project = serializer.save()
                logger.info(f"Project {pk} updated successfully")
                
                response_serializer = ProjectDetailSerializer(project, context={'request': request})
                return Response(response_serializer.data)
            else:
                logger.warning(f"Project {pk} update failed - validation errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Error updating project {pk}: {str(e)}", exc_info=True)
            return Response(
                {'detail': 'An error occurred while updating the project'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, pk):
        """
        Perform partial update of a project (update only provided fields).
        
        Only the project owner can update the project. Only provided
        fields are updated (partial=True).
        
        Args:
            request: HTTP request object containing fields to update
            pk: Primary key of the project to update
            
        Returns:
            Response: JSON response with updated project or errors
            
        Status Codes:
            200: Project updated successfully
            400: Invalid data provided
            403: User is not the project owner
            404: Project not found
            500: Server error during update
        """
        try:
            logger.info(f"Partial update requested for project {pk} by user {request.user}")
            project = self.get_object(pk)
            
            # Check ownership
            if project.owner != request.user:
                logger.warning(f"Unauthorized partial update attempt on project {pk} by user {request.user}")
                return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)

            logger.debug(f"Partial update data for project {pk}: {request.data}")
            serializer = ProjectWriteSerializer(
                project, 
                data=request.data, 
                partial=True, 
                context={'request': request}
            )
            
            if serializer.is_valid():
                project = serializer.save()
                logger.info(f"Project {pk} partially updated successfully")
                
                response_serializer = ProjectDetailSerializer(project, context={'request': request})
                return Response(response_serializer.data)
            else:
                logger.warning(f"Project {pk} partial update failed - validation errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Error partially updating project {pk}: {str(e)}", exc_info=True)
            return Response(
                {'detail': 'An error occurred while updating the project'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, pk):
        """
        Delete a project.
        
        Only the project owner can delete the project. This performs
        a hard delete from the database.
        
        Args:
            request: HTTP request object
            pk: Primary key of the project to delete
            
        Returns:
            Response: Empty response on success
            
        Status Codes:
            204: Project deleted successfully
            403: User is not the project owner
            404: Project not found
            500: Server error during deletion
        """
        try:
            logger.info(f"Delete requested for project {pk} by user {request.user}")
            project = self.get_object(pk)
            
            # Check ownership
            if project.owner != request.user:
                logger.warning(f"Unauthorized delete attempt on project {pk} by user {request.user}")
                return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
            
            project_title = project.title  # Store for logging before deletion
            project.delete()
            logger.info(f"Project '{project_title}' (ID: {pk}) deleted successfully by user {request.user}")
            
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            logger.error(f"Error deleting project {pk}: {str(e)}", exc_info=True)
            return Response(
                {'detail': 'An error occurred while deleting the project'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
