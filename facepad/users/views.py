from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from users.models import FriendRequest

from .serializers import FriendRequestSerializer, UserSerializer


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class RequestFriend(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def perform_create(self, serializer):
        query = (
            FriendRequest.objects.filter(
                requestee__username=serializer.validated_data["requestee"]
            )
            .filter(requestor=self.request.user)
            .filter(status="active")
        )
        if query.exists():
            raise ValidationError("Friend request is still active")
        serializer.save(requestor=self.request.user)  # type: ignore
