from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

REGISTER_USER_URL = reverse('users:register')
LOGIN_USER_URL = reverse('users:login')
REFRESH_TOKEN_URL = reverse('users:token_refresh')

# Create your tests here.
class UserRegistrationAPITest(TestCase):
    """Test the User Regitration API"""
    
    def setUp(self):
        self.client = APIClient()
        self.user_model = get_user_model()
        self.user_payload = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'jdoe',
            'email': 'john.doe@gmail.com',
            'password': 'secret',
            'date_of_birth': '1990-02-14'
        }
        self.copy_username_payload = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'jdoe',
            'email': 'john_doe@gmail.com',
            'password': 'secret',
            'date_of_birth': '1990-02-14'
        }
        self.copy_email_payload = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'john.doe@gmail.com',
            'password': 'secret',
            'date_of_birth': '1990-02-14'
        }
        
    def test_register_user(self):
        """
        Testing to see if we post to the register user url that we get 
        """
        payload = self.user_payload
        self.client.post(REGISTER_USER_URL, payload)
        
        exists = self.user_model.objects.filter(username = payload['username']).exists()
        self.assertTrue(exists)
        
    def test_register_unique_username(self):
        """Testing to make sure that the username is unique
        """
        self.client.post(REGISTER_USER_URL, self.user_payload)
        post_bad = self.client.post(REGISTER_USER_URL, self.copy_username_payload)
        self.assertEqual(post_bad.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_register_unique_email(self):
        """Testing to make sure that the email is unique
        """
        self.client.post(REGISTER_USER_URL, self.user_payload)
        post_bad = self.client.post(REGISTER_USER_URL, self.copy_email_payload)
        self.assertEqual(post_bad.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_regular_user(self):
        """Testing to make sure that when a user registers they are only a regular user
        """
        self.client.post(REGISTER_USER_URL, self.user_payload)
        user = self.user_model.objects.get(username=self.user_payload['username'])
        self.assertEqual(user.user_type, 'regular') #type: ignore
        
        
class UserLoginAPITest(TestCase):
    """Test the Login API
    """
    def setUp(self):
        self.client = APIClient()
        self.user_model = get_user_model()
        
        payload = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'jdoe',
            'email': 'john.doe@gmail.com',
            'password': 'secret',
            'date_of_birth': '1990-02-14'
        }
        self.client.post(REGISTER_USER_URL, payload)
        
    def test_login_returns_jwt(self):
        payload = {
            'username': 'jdoe',
            'password': 'secret',
        }
        login = self.client.post(LOGIN_USER_URL, payload)
        self.assertTrue('access' in login.data) #type: ignore
        self.assertTrue('refresh' in login.data) #type: ignore
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        
    def test_refresh_returns_jwt(self):
        payload_login = {
            'username': 'jdoe',
            'password': 'secret',
        }
        login = self.client.post(LOGIN_USER_URL, payload_login)
        payload = {
            'refresh': login.data['refresh'] #type: ignore
        }
        refresh = self.client.post(REFRESH_TOKEN_URL, payload)
        self.assertTrue('access' in refresh.data) #type: ignore
        
        
class GetUserInfo(TestCase):
    """This is a test case to test the requirements for the user info get endpoint
    """
    def setUp(self):
        self.client = APIClient()
        self.user_model = get_user_model()
        
        self.payload_user = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'jdoe',
            'email': 'john.doe@gmail.com',
            'password': 'secret',
            'date_of_birth': '1990-02-14'
        }
        payload_login = {
            'username': 'jdoe',
            'password': 'secret',
        }
        self.client.post(REGISTER_USER_URL, self.payload_user)
        login = self.client.post(LOGIN_USER_URL, payload_login)


class CreateFriendRequest(TestCase):
    """This is a test case to test the create friend request endpoint
    """
    def setUp(self):
        self.client = APIClient()
        self.user_model = get_user_model()
        self.payload_user = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'jdoe',
            'email': 'john.doe@gmail.com',
            'password': 'secret',
            'date_of_birth': '1990-02-14'
        }
        self.payload_friend = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'username': 'jdoe2',
            'email': 'jane.doe@gmail.com',
            'password': 'secret',
            'date_of_birth': '1993-02-14'
        }
        self.client.post(REGISTER_USER_URL, self.payload_user)
        self.client.post(REGISTER_USER_URL, self.payload_friend)
        login