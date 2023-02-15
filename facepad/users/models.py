from datetime import date

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Extended user model to give extra needed functionality of user"""
    USER_TYPE_CHOICES = [
        ('regular', 'Regular'),
        ('admin', 'Admin')
    ]
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    friends = models.ManyToManyField('self', blank=True)
    user_type = models.CharField(
        max_length=7,
        choices=USER_TYPE_CHOICES,
        default='regular',
    )


class FriendRequest(models.Model):
    """Friend request model to store friend request data
    Defaults to active since when the friend is requested it is active
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    requestor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    requestee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=8,
        choices=STATUS_CHOICES,
        default='active'
    )
    created_date = models.DateField(
        default=date.today
        )
