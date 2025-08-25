from django.urls import path
from apps.catalog.apis.medias import ProjectMediaUploadAPIView
from apps.catalog.apis.projects_apis import ProjectDetailAPIView, ProjectListCreateAPIView
from apps.catalog.apis.tags import TagDetailAPIView, TagListCreateAPIView 

urlpatterns = [
    path('', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/<int:pk>', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('projects/<int:pk>/upload-media', ProjectMediaUploadAPIView.as_view(), name='project-upload-media'),

    path('tags', TagListCreateAPIView.as_view(), name='tag-list-create'),
    path('tags/<int:pk>', TagDetailAPIView.as_view(), name='tag-detail'),
]
