from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from users.models import FriendRequest

from .serializers import FriendRequestSerializer, UserSerializer


# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class RequestFriend(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def post(self, request, *args, **kwargs):
        query = (
            FriendRequest.objects.filter(requestee__username=request.data["requestee"])
            .filter(requestor=self.request.user)
            .filter(status="active")
        )
        if query.exists():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Friend request is still active"},
            )
        requestee = get_user_model().objects.get(username=request.data["requestee"])
        request.data["requestee"] = requestee.pk
        request.data["requestor"] = self.request.user.pk
        return super().post(request, *args, **kwargs)
