from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Project(models.Model):

    STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('ongoing', 'Ongoing'),
    ('done', 'Completed'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    summary = models.TextField()
    location = models.CharField(max_length=160, blank=True)
    area_sqm = models.PositiveIntegerField(null=True, blank=True)
    budget = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='draft')
    featured = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='projects/covers/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
