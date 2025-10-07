from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

from config.settings import base
from utility.bases.base_model import BaseModel

from catalog.models.tags import Tag


class Project(BaseModel):

    STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('ongoing', 'Ongoing'),
    ('done', 'Completed'),
    ]

    owner = models.ForeignKey(base.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True, null=True)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            # تبدیل title به slug
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1
            # اطمینان از یکتا بودن
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{num}"
                num += 1
            self.slug = slug
        super().save(*args, **kwargs)