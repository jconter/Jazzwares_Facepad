from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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


class GetUserView(generics.RetrieveUpdateDestroyAPIView):
    """View to get user info"""

    permission_classes = [IsAuthenticated]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"
    lookup_url_kwarg = "username"

    def get(self, request, *args, **kwargs):
        desired_user = get_user_model().objects.get(
            username=self.kwargs[self.lookup_url_kwarg]
        )
        if request.user.user_type == "admin":
            return super().get(request, *args, **kwargs)
        elif desired_user == self.request.user:
            return super().get(request, *args, **kwargs)
        elif desired_user in self.request.user.friends.all():  # type: ignore
            return super().get(request, *args, **kwargs)
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND, data={"message", "user not found"}
            )

    def put(self, request, *args, **kwargs):
        if request.user.user_type == "admin":
            return super().put(request, *args, **kwargs)
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND, data={"message", "user not found"}
            )

    def patch(self, request, *args, **kwargs):
        if request.user.user_type == "admin":
            return super().patch(request, *args, **kwargs)
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND, data={"message", "user not found"}
            )

    def delete(self, request, *args, **kwargs):
        if request.user.user_type == "admin":
            return super().delete(request, *args, **kwargs)
        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND, data={"message", "user not found"}
            )


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
