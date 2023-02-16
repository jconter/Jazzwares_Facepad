from django.urls import path

from .views import CreateCommentView, CreateContentView, GetFriendContentView

app_name = "content"

urlpatterns = [
    path("content/create/", CreateContentView.as_view(), name="content"),
    path("content/get/<owner>", GetFriendContentView.as_view(), name="get_friend"),
    path(
        "content/comment/<content>/",
        CreateCommentView.as_view(),
        name="content_comment",
    ),
    path(
        "content/comment/<content>/<parent_comment>/",
        CreateCommentView.as_view(),
        name="content_comment_comment",
    ),
]
