from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework import generics

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer