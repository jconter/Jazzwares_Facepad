"""Datebase Models for the Content application of this system
"""

from datetime import date

from django.conf import settings
from django.db import models


class Content(models.Model):
    """Model for the content that will be uploaded to tha application"""

    media = models.FileField(upload_to="content/%Y/%m/%d/")
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="content"
    )
    created_date = models.DateField(default=date.today)


class Comment(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.ForeignKey(
        Content, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.CharField(max_length=150)
    created_date = models.DateField(default=date.today)
    parent_comment = models.ManyToManyField("self", blank=True)
