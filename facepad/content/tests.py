"""Tests for the content app"""
import tempfile
from datetime import date

from content.models import Content
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

REGISTER_USER_URL = reverse("users:register")
LOGIN_USER_URL = reverse("users:login")


class ContentUploadAPITest(TestCase):
    """Testing the Content Upload API endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.client_friend = APIClient()
        self.create_content_url = reverse("content:create")
        self.tmpfile = tempfile.NamedTemporaryFile(suffix=".jpg")
        image = Image.new("RGB", (100, 100))
        image.save(self.tmpfile.name)
        self.payload_content = {
            "media": self.tmpfile,
            "title": "Super Cool Title",
            "description": "this is the best description in the world",
        }
        self.payload_user = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "jdoe",
            "email": "john.doe@gmail.com",
            "password": "secret",
            "date_of_birth": "1990-02-14",
        }
        self.payload_login = {
            "username": "jdoe",
            "password": "secret",
        }
        self.client.post(REGISTER_USER_URL, self.payload_user)
        login = self.client.post(LOGIN_USER_URL, self.payload_login)
        self.auth_token = login.data["access"]  # type: ignore
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_token)

    def test_create_content(self):
        """Make sure you can create content and it is what you expected"""
        post = self.client.post(
            self.create_content_url, self.payload_content, format="multipart"
        )
        content = Content.objects.get(id=1)
        user = get_user_model().objects.get(id=1)
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(content.title, self.payload_content["title"])
        self.assertEqual(content.description, self.payload_content["description"])
        self.assertEqual(content.owner, user)
        self.assertEqual(content.created_date, date.today())

    def test_create_content_auth(self):
        """Make sure that only authed users can create content"""
        self.client.credentials()  # type: ignore
        post = self.client.post(self.create_content_url, self.payload_content)
        self.assertEqual(post.status_code, status.HTTP_401_UNAUTHORIZED)
