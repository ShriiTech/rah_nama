from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from utility.bases.base_model import BaseModel

class Tag(BaseModel):

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
