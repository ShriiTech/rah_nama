from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from apps.catalog.models import Project
from apps.catalog.serializers.projects import (
    ProjectListSerializer, ProjectDetailSerializer, ProjectWriteSerializer,
)


class ProjectListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        projects = Project.objects.all().select_related('owner').prefetch_related('tags', 'media')
        serializer = ProjectListSerializer(projects, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectWriteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            project = serializer.save()
            return Response(ProjectDetailSerializer(project, context={'request': request}).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Project.objects.prefetch_related('tags', 'media'), pk=pk)

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        if project.owner != request.user:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProjectWriteSerializer(project, data=request.data, partial=False, context={'request': request})
        if serializer.is_valid():
            project = serializer.save()
            return Response(ProjectDetailSerializer(project, context={'request': request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        project = self.get_object(pk)
        if project.owner != request.user:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProjectWriteSerializer(project, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            project = serializer.save()
            return Response(ProjectDetailSerializer(project, context={'request': request}).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        project = self.get_object(pk)
        if project.owner != request.user:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    