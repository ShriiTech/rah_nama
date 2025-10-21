from django.db import models
from django.utils.text import slugify
from django.conf import settings

from utility.bases.base_model import BaseModel
from catalog.models.tags import Tag


class Project(BaseModel):
    """
    Represents a construction project with detailed information such as 
    owner, municipal file number, location, and project status.
    """

    MUNICIPAL_FILE_NUMBER_HELP = "Unique municipal file number for each project."

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),
        ("archived", "Archived"),
        ("active", "Active"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name="Project Owner",
    )

    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True, null=True)
    summary = models.TextField()
    location = models.CharField(max_length=160, blank=True)
    area_sqm = models.PositiveIntegerField(null=True, blank=True)
    budget = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    municipal_file_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Municipal File Number",
        help_text=MUNICIPAL_FILE_NUMBER_HELP,
    )

    owner_name = models.CharField(max_length=100, verbose_name="Owner Name")
    total_area = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Total Project Area (m²)"
    )
    floors_count = models.PositiveIntegerField(verbose_name="Number of Floors")

    start_date = models.DateField(verbose_name="Contract Start Date", null=True, blank=True)
    end_date = models.DateField(verbose_name="Contract End Date", null=True, blank=True)
    address = models.TextField(verbose_name="Project Address")

    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default="active",
        verbose_name="Project Status",
    )

    featured = models.BooleanField(default=False)
    cover = models.ImageField(upload_to="projects/covers/", null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="projects")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["municipal_file_number"]),
            models.Index(fields=["status"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return f"{self.municipal_file_number} - {self.owner_name}"

    def save(self, *args, **kwargs):
        """
        Auto-generate a unique slug based on the project title if not provided.
        """
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        """
        Generate a unique slug from the project title.
        """
        base_slug = slugify(self.title)
        slug = base_slug
        num = 1
        while Project.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{num}"
            num += 1
        return slug
