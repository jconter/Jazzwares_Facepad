from content.models import Comment, Content, Rating
from content.serializers import CommentSerializer, ContentSerializer, RatingSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# Create your views here.
class CreateContentView(generics.ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.queryset = Content.objects.filter(owner=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GetFriendContentView(generics.ListAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "owner"
    lookup_url_kwarg = "owner"

    def get_queryset(self):
        self.queryset = Content.objects.filter(
            owner__username=self.kwargs[self.lookup_url_kwarg]
        )
        return super().get_queryset()

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
                status=status.HTTP_404_NOT_FOUND,
                data={"message", "user content not found"},
            )


class CreateListCommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.queryset = Comment.objects.filter(
            content__title=self.kwargs.get("content")
        )
        return super().get_queryset()

    def perform_create(self, serializer):
        content = Content.objects.get(title=self.kwargs.get("content"))
        if self.kwargs.get("parent_comment"):
            parent_comment = Comment.objects.get(
                id=int(self.kwargs.get("parent_comment"))
            )
            serializer.save(
                owner=self.request.user,
                content=content,
                parent_comment=[parent_comment],
            )
        else:
            serializer.save(
                owner=self.request.user,
                content=content,
            )

    def post(self, request, *args, **kwargs):
        content = Content.objects.get(title=self.kwargs.get("content"))
        content_owner = get_user_model().objects.get(id=content.owner.id)
        not_friend = self.request.user not in content_owner.friends.all()  # type: ignore
        not_self = self.request.user != content_owner
        if not_friend and not_self:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return super().post(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        content = Content.objects.get(title=self.kwargs.get("content"))
        content_owner = get_user_model().objects.get(id=content.owner.id)
        not_friend = self.request.user not in content_owner.friends.all()  # type: ignore
        not_admin = request.user.user_type != "admin"
        not_self = self.request.user != content_owner
        if not_friend and not_self and not_admin:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return super().list(request, *args, **kwargs)


class CreateListRatingsAPIView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.queryset = Rating.objects.filter(content__title=self.kwargs.get("content"))
        return super().get_queryset()

    def perform_create(self, serializer):
        content = Content.objects.get(title=self.kwargs.get("content"))
        serializer.save(
            owner=self.request.user,
            content=content,
        )

    def post(self, request, *args, **kwargs):
        content = Content.objects.get(title=self.kwargs.get("content"))
        content_owner = get_user_model().objects.get(id=content.owner.id)
        not_friend = self.request.user not in content_owner.friends.all()  # type: ignore
        not_self = self.request.user != content_owner
        if not_friend and not_self:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return super().post(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        content = Content.objects.get(title=self.kwargs.get("content"))
        content_owner = get_user_model().objects.get(id=content.owner.id)
        not_friend = self.request.user not in content_owner.friends.all()  # type: ignore
        not_admin = request.user.user_type != "admin"
        not_self = self.request.user != content_owner
        if not_friend and not_self and not_admin:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return super().list(request, *args, **kwargs)
