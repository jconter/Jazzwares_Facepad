from django.urls import path

from .views import (
    CreateContentView,
    CreateListCommentView,
    CreateListRatingsAPIView,
    GetFriendContentView,
)

app_name = "content"

urlpatterns = [
    path("content/create/", CreateContentView.as_view(), name="content"),
    path("content/get/<owner>", GetFriendContentView.as_view(), name="get_friend"),
    path(
        "content/comment/<content>/",
        CreateListCommentView.as_view(),
        name="content_comment",
    ),
    path(
        "content/comment/<content>/<parent_comment>/",
        CreateListCommentView.as_view(),
        name="content_comment_comment",
    ),
    path(
        "content/rating/<content>/",
        CreateListRatingsAPIView.as_view(),
        name="ratings",
    ),
]
