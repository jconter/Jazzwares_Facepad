from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer


# Create your views here.
class RegisterView(generics.CreateAPIView):
    """View to register a new User, only has post method"""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class GetUserView(generics.RetrieveAPIView):
    """View to get user info"""
    permission_classes=[IsAuthenticated]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
