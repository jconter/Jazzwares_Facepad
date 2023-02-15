from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

REGISTER_USER_URL = reverse('users:register')

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
        
        