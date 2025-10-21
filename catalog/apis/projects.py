import logging
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema_view

from catalog.models import Project
from catalog.schema.projects import ProjectDetailSchema, ProjectListCreateSchema
from catalog.serializers.projects import (
    ProjectListSerializer,
    ProjectDetailSerializer,
    ProjectWriteSerializer,
)

logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------
# 🔹 Project List & Create
# ------------------------------------------------------------------------
@extend_schema_view(
    get=ProjectListCreateSchema.list_schema,
    post=ProjectListCreateSchema.create_schema,
)
class ProjectListCreateAPIView(APIView):
    """
    API View for listing all projects and creating new ones.

    - GET: Public list (filtering, search, ordering supported)
    - POST: Create project (authenticated users only)
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        logger.info("Fetching projects for listing")

        queryset = Project.objects.select_related("owner").prefetch_related("tags")

        # --- Filtering ---
        status_param = request.query_params.get("status")
        featured_param = request.query_params.get("featured")
        search_param = request.query_params.get("search")
        ordering_param = request.query_params.get("ordering")

        if status_param:
            queryset = queryset.filter(status=status_param)
        if featured_param in ["true", "1"]:
            queryset = queryset.filter(featured=True)
        if search_param:
            queryset = queryset.filter(
                Q(title__icontains=search_param)
                | Q(municipal_file_number__icontains=search_param)
                | Q(owner_name__icontains=search_param)
                | Q(address__icontains=search_param)
            )
        if ordering_param:
            queryset = queryset.order_by(ordering_param)
        else:
            queryset = queryset.order_by("-created_at")

        serializer = ProjectListSerializer(queryset, many=True, context={"request": request})
        logger.debug(f"Returning {len(serializer.data)} projects")
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        logger.info(f"Creating new project by user {request.user}")
        serializer = ProjectWriteSerializer(data=request.data, context={"request": request})

        if not serializer.is_valid():
            logger.warning(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        project = serializer.save(owner=request.user)
        logger.info(f"Project created successfully (ID={project.id})")

        response_data = ProjectDetailSerializer(project, context={"request": request}).data
        return Response(response_data, status=status.HTTP_201_CREATED)


# ------------------------------------------------------------------------
# 🔹 Project Detail (Retrieve, Update, Delete)
# ------------------------------------------------------------------------
@extend_schema_view(
    get=ProjectDetailSchema.retrieve_schema,
    put=ProjectDetailSchema.update_schema,
    patch=ProjectDetailSchema.update_schema,
    delete=ProjectDetailSchema.delete_schema,
)
class ProjectDetailAPIView(APIView):
    """
    Retrieve, update, or delete a specific project.

    Supports both numeric ID and slug as identifier.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk_or_slug):
        """Fetch project by ID or slug."""
        lookup = {"pk": pk_or_slug} if str(pk_or_slug).isdigit() else {"slug": pk_or_slug}
        project = get_object_or_404(
            Project.objects.select_related("owner").prefetch_related("tags"), **lookup
        )
        return project

    def get(self, request, pk_or_slug):
        logger.info(f"Fetching project details for {pk_or_slug}")
        project = self.get_object(pk_or_slug)
        serializer = ProjectDetailSerializer(project, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk_or_slug):
        return self._update_project(request, pk_or_slug, partial=False)

    def patch(self, request, pk_or_slug):
        return self._update_project(request, pk_or_slug, partial=True)

    def _update_project(self, request, pk_or_slug, partial=False):
        project = self.get_object(pk_or_slug)

        if project.owner != request.user:
            logger.warning(f"Unauthorized update attempt by {request.user} on {project.id}")
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProjectWriteSerializer(
            project, data=request.data, partial=partial, context={"request": request}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        project = serializer.save()
        logger.info(f"Project {project.id} updated successfully")

        response_data = ProjectDetailSerializer(project, context={"request": request}).data
        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request, pk_or_slug):
        project = self.get_object(pk_or_slug)

        if project.owner != request.user:
            logger.warning(f"Unauthorized delete attempt by {request.user} on {project.id}")
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        project.delete()
        logger.info(f"Project {pk_or_slug} deleted successfully")
        return Response(status=status.HTTP_204_NO_CONTENT)
