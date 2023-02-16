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
        self.create_content_url = reverse("content:content")
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
        post = self.client.post(
            self.create_content_url, self.payload_content, format="multipart"
        )
        self.assertEqual(post.status_code, status.HTTP_401_UNAUTHORIZED)


class ContentGetAPITest(TestCase):
    """Testing to Get method for the Content endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.client_other = APIClient()
        self.create_content_url = reverse("content:content")
        self.tmpfile = tempfile.NamedTemporaryFile(suffix=".jpg")
        image = Image.new("RGB", (100, 100))
        image.save(self.tmpfile.name)
        self.tmpfile2 = tempfile.NamedTemporaryFile(suffix=".jpg")
        image = Image.new("RGB", (100, 100))
        image.save(self.tmpfile2.name)
        self.payload_content = {
            "media": self.tmpfile,
            "title": "Super Cool Title",
            "description": "This is the best description in the world!",
        }
        self.payload_content_other = {
            "media": self.tmpfile2,
            "title": "Super Cool Second Title",
            "description": "This is the best description in the world gwow!",
        }
        self.payload_user = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "jdoe",
            "email": "john.doe@gmail.com",
            "password": "secret",
            "date_of_birth": "1990-02-14",
        }
        self.payload_user_other = {
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "jdoe2",
            "email": "jane.doe@gmail.com",
            "password": "secret",
            "date_of_birth": "1993-01-21",
        }
        self.payload_login = {
            "username": "jdoe",
            "password": "secret",
        }
        self.payload_login_other = {
            "username": "jdoe2",
            "password": "secret",
        }
        self.client.post(REGISTER_USER_URL, self.payload_user)
        login = self.client.post(LOGIN_USER_URL, self.payload_login)
        self.auth_token = login.data["access"]  # type: ignore
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_token)
        self.client_other.post(REGISTER_USER_URL, self.payload_user_other)
        login = self.client_other.post(LOGIN_USER_URL, self.payload_login_other)
        self.auth_token = login.data["access"]  # type: ignore
        self.client_other.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_token)
        self.client.post(
            self.create_content_url, self.payload_content, format="multipart"
        )
        self.client_other.post(
            self.create_content_url, self.payload_content_other, format="multipart"
        )

    def test_user_can_get_their_content(self):
        """Test to make sure that user can get their own content"""
        get = self.client.get(self.create_content_url, format="json")
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertEqual(
            get.data[0]["title"], self.payload_content["title"]  # type: ignore
        )

    def test_user_cant_get_other_content(self):
        """Test to make sure user isn't geting someone elses content"""
        get = self.client_other.get(self.create_content_url, format="json")
        self.assertEqual(get.status_code, status.HTTP_200_OK)  # type: ignore
        self.assertNotEqual(
            get.data[0]["title"], self.payload_content["title"]  # type: ignore
        )


class ContentGetFriendAPITest(TestCase):
    """Testing to Get method for the Friend Content endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.client_friend = APIClient()
        self.client_other = APIClient()
        self.create_content_url = reverse("content:content")
        self.tmpfile = tempfile.NamedTemporaryFile(suffix=".jpg")
        image = Image.new("RGB", (100, 100))
        image.save(self.tmpfile.name)
        self.tmpfile2 = tempfile.NamedTemporaryFile(suffix=".jpg")
        image = Image.new("RGB", (100, 100))
        image.save(self.tmpfile2.name)
        self.tmpfile3 = tempfile.NamedTemporaryFile(suffix=".jpg")
        image = Image.new("RGB", (100, 100))
        image.save(self.tmpfile3.name)
        self.payload_content = {
            "media": self.tmpfile,
            "title": "Super Cool Title",
            "description": "This is the best description in the world!",
        }
        self.payload_content_friend = {
            "media": self.tmpfile2,
            "title": "Super Cool Second Title",
            "description": "This is the best description in the world dang!",
        }
        self.payload_content_other = {
            "media": self.tmpfile3,
            "title": "Super Cool Third Title",
            "description": "This is the best description in the world gwow!",
        }
        self.payload_user = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "jdoe",
            "email": "john.doe@gmail.com",
            "password": "secret",
            "date_of_birth": "1990-02-14",
        }
        self.payload_friend = {
            "first_name": "Best",
            "last_name": "Friend",
            "username": "bfriend",
            "email": "best.friend@gmail.com",
            "password": "secret",
            "date_of_birth": "1990-07-14",
        }
        self.payload_user_other = {
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "jdoe2",
            "email": "jane.doe@gmail.com",
            "password": "secret",
            "date_of_birth": "1993-01-21",
        }
        self.payload_login = {
            "username": "jdoe",
            "password": "secret",
        }
        self.payload_login_friend = {
            "username": "bfriend",
            "password": "secret",
        }
        self.payload_login_other = {
            "username": "jdoe2",
            "password": "secret",
        }
        self.client.post(REGISTER_USER_URL, self.payload_user)
        login = self.client.post(LOGIN_USER_URL, self.payload_login)
        self.auth_token = login.data["access"]  # type: ignore
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_token)
        self.client_friend.post(REGISTER_USER_URL, self.payload_friend)
        login = self.client.post(LOGIN_USER_URL, self.payload_login_friend)
        self.auth_token = login.data["access"]  # type: ignore
        self.client_friend.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_token)
        self.client_other.post(REGISTER_USER_URL, self.payload_user_other)
        login = self.client_other.post(LOGIN_USER_URL, self.payload_login_other)
        self.auth_token = login.data["access"]  # type: ignore
        self.client_other.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_token)
        self.client.post(
            self.create_content_url, self.payload_content, format="multipart"
        )
        self.client_friend.post(
            self.create_content_url, self.payload_content_friend, format="multipart"
        )
        self.client_other.post(
            self.create_content_url, self.payload_content_other, format="multipart"
        )
        user = get_user_model().objects.get(username="jdoe")
        friend = get_user_model().objects.get(username="bfriend")
        friend.friends.add(user)  # type: ignore

    def test_user_can_get_friends_content(self):
        """Test to make sure you can get friend's content"""
        get_friend_content_url = reverse(
            "content:get_friend",
            kwargs={"owner": self.payload_friend["username"]},
        )
        get = self.client.get(get_friend_content_url, format="json")
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertEqual(
            get.data[0]["title"],  # type: ignore
            self.payload_content_friend["title"],
        )

    def test_user_get_friend_content_authed(self):
        """Test to make sure you can get friend's content"""
        self.client.credentials()  # type: ignore
        get_friend_content_url = reverse(
            "content:get_friend",
            kwargs={"owner": self.payload_friend["username"]},
        )
        get = self.client.get(get_friend_content_url, format="json")
        self.assertEqual(get.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_get_non_friend_content(self):
        """Test to make sure user cannot get non friend data"""
        get_friend_content_url = reverse(
            "content:get_friend",
            kwargs={"owner": self.payload_user_other["username"]},
        )
        get = self.client.get(get_friend_content_url, format="json")
        self.assertEqual(get.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_get_self_content(self):
        """Test to make sure you can get self content"""
        get_friend_content_url = reverse(
            "content:get_friend",
            kwargs={"owner": self.payload_user["username"]},
        )
        get = self.client.get(get_friend_content_url, format="json")
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertEqual(
            get.data[0]["title"],  # type: ignore
            self.payload_content["title"],
        )


class CommentAPITest(TestCase):
    """Test Case to test the Create New Comment Endpoint"""

    def setUp(self):
        self.client = APIClient()
        self.client_friend = APIClient()
        self.client_other = APIClient()
        self.create_content_url = reverse("content:content")
        self.tmpfile = tempfile.NamedTemporaryFile(suffix=".jpg")
        image = Image.new("RGB", (100, 100))
        image.save(self.tmpfile.name)
        self.tmpfile2 = tempfile.NamedTemporaryFile(suffix=".jpg")
        image = Image.new("RGB", (100, 100))
        image.save(self.tmpfile2.name)
        self.tmpfile3 = tempfile.NamedTemporaryFile(suffix=".jpg")
        image = Image.new("RGB", (100, 100))
        image.save(self.tmpfile3.name)
        self.payload_content = {
            "media": self.tmpfile,
            "title": "Super Cool Title",
            "description": "This is the best description in the world!",
        }
        self.payload_content_friend = {
            "media": self.tmpfile2,
            "title": "Super Cool Second Title",
            "description": "This is the best description in the world dang!",
        }
        self.payload_content_other = {
            "media": self.tmpfile3,
            "title": "Super Cool Third Title",
            "description": "This is the best description in the world gwow!",
        }
        self.payload_user = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "jdoe",
            "email": "john.doe@gmail.com",
            "password": "secret",
            "date_of_birth": "1990-02-14",
        }
        self.payload_friend = {
            "first_name": "Best",
            "last_name": "Friend",
            "username": "bfriend",
            "email": "best.friend@gmail.com",
            "password": "secret",
            "date_of_birth": "1990-07-14",
        }
        self.payload_user_other = {
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "jdoe2",
            "email": "jane.doe@gmail.com",
            "password": "secret",
            "date_of_birth": "1993-01-21",
        }
        self.payload_login = {
            "username": "jdoe",
            "password": "secret",
        }
        self.payload_login_friend = {
            "username": "bfriend",
            "password": "secret",
        }
        self.payload_login_other = {
            "username": "jdoe2",
            "password": "secret",
        }
        self.payload_comment = {
            "text": "that was amazing content!",
        }
        self.payload_comment_comment = {
            "text": "what an amazing comment!",
        }
        self.client.post(REGISTER_USER_URL, self.payload_user)
        login = self.client.post(LOGIN_USER_URL, self.payload_login)
        self.auth_token = login.data["access"]  # type: ignore
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_token)
        self.client_friend.post(REGISTER_USER_URL, self.payload_friend)
        login = self.client.post(LOGIN_USER_URL, self.payload_login_friend)
        self.auth_token = login.data["access"]  # type: ignore
        self.client_friend.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_token)
        self.client_other.post(REGISTER_USER_URL, self.payload_user_other)
        login = self.client_other.post(LOGIN_USER_URL, self.payload_login_other)
        self.auth_token = login.data["access"]  # type: ignore
        self.client_other.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_token)
        self.client.post(
            self.create_content_url, self.payload_content, format="multipart"
        )
        self.client_friend.post(
            self.create_content_url, self.payload_content_friend, format="multipart"
        )
        self.client_other.post(
            self.create_content_url, self.payload_content_other, format="multipart"
        )
        user = get_user_model().objects.get(username="jdoe")
        friend = get_user_model().objects.get(username="bfriend")
        friend.friends.add(user)  # type: ignore
        friend.save()

    def test_create_comment_successfully(self):
        """Make sure that a user can create a successful comment on a piece
        of conent"""
        create_comment_url = reverse(
            "content:content_comment", kwargs={"content": self.payload_content["title"]}
        )
        post = self.client.post(create_comment_url, self.payload_comment, format="json")
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.data["text"], self.payload_comment["text"])  # type: ignore

    def test_create_friendcomment_successfully(self):
        """Make sure that a user can create a successful comment on a friend's piece
        of conent"""
        create_comment_url = reverse(
            "content:content_comment",
            kwargs={"content": self.payload_content_friend["title"]},
        )
        post = self.client.post(create_comment_url, self.payload_comment, format="json")
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post.data["text"], self.payload_comment["text"])  # type: ignore

    def test_create_comment_authed(self):
        """Make sure user is authed when making comment"""
        self.client.credentials()  # type: ignore
        create_comment_url = reverse(
            "content:content_comment", kwargs={"content": self.payload_content["title"]}
        )
        post = self.client.post(create_comment_url, self.payload_comment, format="json")
        self.assertEqual(post.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_on_comment_successfully(self):
        """Make sure that you can successfully create a comment of a comment"""
        create_comment_url = reverse(
            "content:content_comment", kwargs={"content": self.payload_content["title"]}
        )
        post = self.client.post(create_comment_url, self.payload_comment, format="json")
        create_comment_of_comment_url = reverse(
            "content:content_comment_comment",
            kwargs={
                "content": self.payload_content["title"],
                "parent_comment": str(post.data["id"]),  # type: ignore
            },
        )
        post2 = self.client.post(
            create_comment_of_comment_url, self.payload_comment_comment, format="json"
        )
        self.assertEqual(post2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            post2.data["text"], self.payload_comment_comment["text"]  # type: ignore
        )
        self.assertEqual(post2.data["parent_comment"][0], post.data["id"])  # type: ignore

    def test_create_comment_on_notselforfriend_fail(self):
        """Make sure you can't post a comment on someone who is not your friend"""
        create_comment_url = reverse(
            "content:content_comment",
            kwargs={"content": self.payload_content_other["title"]},
        )
        post = self.client.post(create_comment_url, self.payload_comment, format="json")
        self.assertEqual(post.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_comments_selfcontent_works_successfully(self):
        """Test to make sure you can successfully get comments on self posted content"""
        create_comment_url = reverse(
            "content:content_comment", kwargs={"content": self.payload_content["title"]}
        )
        self.client.post(create_comment_url, self.payload_comment, format="json")
        get_comment_url = reverse(
            "content:content_comment",
            kwargs={"content": self.payload_content["title"]},
        )
        get = self.client.get(get_comment_url, format="json")
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertEqual(get.data[0]["text"], self.payload_comment["text"])  # type: ignore

    def test_get_comments_friendcontent_works_successfully(self):
        """Test to make sure you can successfully get friend's content comments"""
        create_comment_url = reverse(
            "content:content_comment",
            kwargs={"content": self.payload_content_friend["title"]},
        )
        self.client.post(create_comment_url, self.payload_comment, format="json")
        get_comment_url = reverse(
            "content:content_comment",
            kwargs={"content": self.payload_content_friend["title"]},
        )
        get = self.client.get(get_comment_url, format="json")
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertEqual(get.data[0]["text"], self.payload_comment["text"])  # type: ignore

    def test_get_comments_friendcontent_auth_fails(self):
        """Test to make sure you can't get comments if you are not authed"""
        self.client.credentials()  # type: ignore
        create_comment_url = reverse(
            "content:content_comment",
            kwargs={"content": self.payload_content_friend["title"]},
        )
        self.client.post(create_comment_url, self.payload_comment, format="json")
        get_comment_url = reverse(
            "content:content_comment",
            kwargs={"content": self.payload_content_friend["title"]},
        )
        get = self.client.get(get_comment_url, format="json")
        self.assertEqual(get.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_comments_othercontent_fails(self):
        """Test to make sure you can't get comments from content
        whose owner is not in your friend group"""
        create_comment_url = reverse(
            "content:content_comment",
            kwargs={"content": self.payload_content_other["title"]},
        )
        self.client.post(create_comment_url, self.payload_comment, format="json")
        get_comment_url = reverse(
            "content:content_comment",
            kwargs={"content": self.payload_content_other["title"]},
        )
        get = self.client.get(get_comment_url, format="json")
        self.assertEqual(get.status_code, status.HTTP_401_UNAUTHORIZED)


class RatingAPITests(TestCase):
    """Test Cases for Ratings API"""

    def setUp(self):
        self.client = APIClient()
        self.client_friend = APIClient()
        self.client_other = APIClient()
        self.create_content_url = reverse("content:content")
        self.tmpfile = tempfile.NamedTemporaryFile(suffix=".jpg")
        image = Image.new("RGB", (100, 100))
        image.save(self.tmpfile.name)
        self.tmpfile2 = tempfile.NamedTemporaryFile(suffix=".jpg")
        image = Image.new("RGB", (100, 100))
        image.save(self.tmpfile2.name)
        self.tmpfile3 = tempfile.NamedTemporaryFile(suffix=".jpg")
        image = Image.new("RGB", (100, 100))
        image.save(self.tmpfile3.name)
        self.payload_content = {
            "media": self.tmpfile,
            "title": "Super Cool Title",
            "description": "This is the best description in the world!",
        }
        self.payload_content_friend = {
            "media": self.tmpfile2,
            "title": "Super Cool Second Title",
            "description": "This is the best description in the world dang!",
        }
        self.payload_content_other = {
            "media": self.tmpfile3,
            "title": "Super Cool Third Title",
            "description": "This is the best description in the world gwow!",
        }
        self.payload_user = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "jdoe",
            "email": "john.doe@gmail.com",
            "password": "secret",
            "date_of_birth": "1990-02-14",
        }
        self.payload_friend = {
            "first_name": "Best",
            "last_name": "Friend",
            "username": "bfriend",
            "email": "best.friend@gmail.com",
            "password": "secret",
            "date_of_birth": "1990-07-14",
        }
        self.payload_user_other = {
            "first_name": "Jane",
            "last_name": "Doe",
            "username": "jdoe2",
            "email": "jane.doe@gmail.com",
            "password": "secret",
            "date_of_birth": "1993-01-21",
        }
        self.payload_login = {
            "username": "jdoe",
            "password": "secret",
        }
        self.payload_login_friend = {
            "username": "bfriend",
            "password": "secret",
        }
        self.payload_login_other = {
            "username": "jdoe2",
            "password": "secret",
        }
        self.payload_rating = {
            "value": "5",
        }
        self.payload_rating_oob = {
            "rating": "10",
        }
        self.payload_rating_low = {
            "rating": "0",
        }
        self.client.post(REGISTER_USER_URL, self.payload_user)
        login = self.client.post(LOGIN_USER_URL, self.payload_login)
        self.auth_token = login.data["access"]  # type: ignore
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_token)
        self.client_friend.post(REGISTER_USER_URL, self.payload_friend)
        login = self.client.post(LOGIN_USER_URL, self.payload_login_friend)
        self.auth_token = login.data["access"]  # type: ignore
        self.client_friend.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_token)
        self.client_other.post(REGISTER_USER_URL, self.payload_user_other)
        login = self.client_other.post(LOGIN_USER_URL, self.payload_login_other)
        self.auth_token = login.data["access"]  # type: ignore
        self.client_other.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_token)
        self.client.post(
            self.create_content_url, self.payload_content, format="multipart"
        )
        self.client_friend.post(
            self.create_content_url, self.payload_content_friend, format="multipart"
        )
        self.client_other.post(
            self.create_content_url, self.payload_content_other, format="multipart"
        )
        user = get_user_model().objects.get(username="jdoe")
        friend = get_user_model().objects.get(username="bfriend")
        friend.friends.add(user)  # type: ignore
        friend.save()

    def test_create_friend_content_rating_successfully(self):
        """Make sure a user can create a content rating of friend's content successfuly"""
        create_rating_url = reverse(
            "content:ratings", kwargs={"content": self.payload_content_friend["title"]}
        )
        post = self.client.post(create_rating_url, self.payload_rating, format="json")
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            post.data["value"], int(self.payload_rating["value"])  # type: ignore
        )

    def test_create_rating_selfcontent_passes(self):
        """Make sure a user cannot create a rating on their own content"""
        create_rating_url = reverse(
            "content:ratings", kwargs={"content": self.payload_content["title"]}
        )
        post = self.client.post(create_rating_url, self.payload_rating, format="json")
        self.assertEqual(post.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            post.data["value"], int(self.payload_rating["value"])  # type: ignore
        )

    def test_create_rating_value_high_fails(self):
        """Make sure user cannot make a rating that is higher than the limit"""
        create_rating_url = reverse(
            "content:ratings", kwargs={"content": self.payload_content_friend["title"]}
        )
        post = self.client.post(
            create_rating_url, self.payload_rating_oob, format="json"
        )
        self.assertEqual(post.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_rating_value_low_fails(self):
        """Make sure user cannot make a rating that is higher than the limit"""
        create_rating_url = reverse(
            "content:ratings", kwargs={"content": self.payload_content_friend["title"]}
        )
        post = self.client.post(
            create_rating_url, self.payload_rating_low, format="json"
        )
        self.assertEqual(post.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_rating_rate_nonfriend_fails(self):
        create_rating_url = reverse(
            "content:ratings", kwargs={"content": self.payload_content_other["title"]}
        )
        post = self.client.post(create_rating_url, self.payload_rating, format="json")
        self.assertEqual(post.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_rating_self_content_successfull(self):
        """Make sure you can get the ratings of your own content"""
        get_rating_url = reverse(
            "content:ratings", kwargs={"content": self.payload_content["title"]}
        )
        self.client.post(get_rating_url, self.payload_rating, format="json")
        get = self.client.get(get_rating_url, format="json")
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertEqual(
            get.data[0]["value"], int(self.payload_rating["value"])  # type: ignore
        )

    def test_get_rating_friend_content_successfull(self):
        """Make sure you can get the ratings of your friends content"""
        get_rating_url = reverse(
            "content:ratings", kwargs={"content": self.payload_content_friend["title"]}
        )
        self.client.post(get_rating_url, self.payload_rating, format="json")
        get = self.client.get(get_rating_url, format="json")
        self.assertEqual(get.status_code, status.HTTP_200_OK)
        self.assertEqual(
            get.data[0]["value"], int(self.payload_rating["value"])  # type: ignore
        )

    def test_get_rating_nonselforfriend_content_fails(self):
        """Make sure you cannot get the ratings of non friends or yourself content"""
        get_rating_url = reverse(
            "content:ratings", kwargs={"content": self.payload_content_other["title"]}
        )
        self.client.post(get_rating_url, self.payload_rating, format="json")
        get = self.client.get(get_rating_url, format="json")
        self.assertEqual(get.status_code, status.HTTP_401_UNAUTHORIZED)
