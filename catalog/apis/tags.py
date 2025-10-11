from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from catalog.models import Tag
from catalog.schema.tags import TagDetailSchema, TagListCreateSchema
from catalog.serializers.projects import TagSerializer

from drf_spectacular.utils import extend_schema_view


TagListCreateAPIView = extend_schema_view(
    get=TagListCreateSchema.list_schema,
    post=TagListCreateSchema.create_schema,
)
class TagListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            tag = serializer.save()
            return Response(TagSerializer(tag).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

TagDetailAPIView = extend_schema_view(
    get=TagDetailSchema.retrieve_schema,
    put=TagDetailSchema.update_schema,
    delete=TagDetailSchema.delete_schema,
)
class TagDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        return get_object_or_404(Tag, pk=pk)

    def get(self, request, pk):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def put(self, request, pk):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            tag = serializer.save()
            return Response(TagSerializer(tag).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        tag = self.get_object(pk)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
