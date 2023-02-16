from content.models import Comment, Content
from content.serializers import CommentSerializer, ContentSerializer
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


class CreateCommentView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

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
