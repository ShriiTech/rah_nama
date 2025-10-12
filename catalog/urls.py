from django.urls import path, include

from catalog.apis.medias import ProjectMediaUploadAPIView
from catalog.apis.projects import ProjectDetailAPIView, ProjectListCreateAPIView
from catalog.apis.tags import TagDetailAPIView, TagListCreateAPIView 

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
    path('projects', ProjectListCreateAPIView.as_view(), name='project-list-create'),
    path('projects/<int:pk>', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('projects/<int:pk>/upload-media', ProjectMediaUploadAPIView.as_view(), name='project-upload-media'),

    path('tags', TagListCreateAPIView.as_view(), name='tag-list-create'),
    
    path('tags/<int:pk>', TagDetailAPIView.as_view(), name='tag-detail'),
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('api/docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Redoc UI
    path('api/redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # بقیه APIها
    path('api/', include('account.urls')),
    path('api/', include('catalog.urls')),
]
