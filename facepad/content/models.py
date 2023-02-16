"""Datebase Models for the Content application of this system
"""

from datetime import date

from django.conf import settings
from django.db import models


class Content(models.Model):
    """Model for the content that will be uploaded to tha application"""

    media = models.FileField(upload_to="content/%Y/%m/%d/")
    title = models.CharField(max_length=150)
    description = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owner"
    )
    created_date = models.DateField(default=date.today)
