# Generated by Django 4.1.7 on 2023-02-15 22:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FriendRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("active", "Active"),
                            ("accepted", "Accepted"),
                            ("rejected", "Rejected"),
                        ],
                        default="active",
                        max_length=8,
                    ),
                ),
                ("created_date", models.DateField(default=datetime.date.today)),
                (
                    "requestee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="requestee",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "requestor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="requestor",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
