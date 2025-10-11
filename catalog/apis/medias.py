from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from catalog.models import Project, Media
from catalog.schema.medias import ProjectMediaUploadSchema
from catalog.serializers.projects import MediaSerializer

from drf_spectacular.utils import extend_schema_view

@extend_schema_view(
    post=ProjectMediaUploadSchema.post_schema
)
class ProjectMediaUploadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        if project.owner != request.user:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)

        files = request.FILES.getlist('files')
        created = []
        for f in files:
            created.append(Media.objects.create(project=project, file=f, type='image'))
        return Response(MediaSerializer(created, many=True, context={'request': request}).data, status=201)
