from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from users.models import FriendRequest

from .serializers import (
    FriendRequestResponseSerializer,
    FriendRequestSerializer,
    UserSerializer,
)


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


class RequestFriend(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

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


class GetFriendRequests(generics.ListAPIView):
    """Endpoint to get a list of active friend requests"""

    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.queryset = FriendRequest.objects.filter(
            requestee=self.request.user
        ).filter(status="active")
        return super().get_queryset()


class FriendRequestResponse(generics.UpdateAPIView):
    """Endpoint to respond to a friend request"""

    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.queryset = FriendRequest.objects.filter(
            requestee=self.request.user
        ).filter(status="active")
        return super().get_queryset()

    def perform_update(self, serializer):
        if serializer.validated_data["status"] == "rejected":
            serializer.save()
        elif serializer.validated_data["status"] == "accepted":
            fq = FriendRequest.objects.get(id=int(self.kwargs["pk"]))
            requestor = get_user_model().objects.get(id=fq.requestor.id)
            requestee = get_user_model().objects.get(id=fq.requestee.id)
            requestee.friends.add(requestor)  # type: ignore
            requestee.save()
            serializer.save()
