from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
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
