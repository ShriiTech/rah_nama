from django.db import models
from apps.catalog.models.projects import Project
from utility.bases.base_model import BaseModel


class Media(BaseModel):
    FILE_TYPES = [
    ('image', 'Image'),
    ('file', 'File'),
    ('video', 'Video'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='media')
    file = models.FileField(upload_to='projects/media/')
    caption = models.CharField(max_length=180, blank=True)
    type = models.CharField(max_length=10, choices=FILE_TYPES, default='image')
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'uploaded_at']

    def __str__(self):
        return f"{self.project.title} - {self.caption or self.file.name}"
    