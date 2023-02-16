from django.urls import path

from .views import CreateContentView, GetFriendContentView

app_name = "content"

urlpatterns = [
    path("content/create/", CreateContentView.as_view(), name="content"),
    path("content/get/<owner>", GetFriendContentView.as_view(), name="get_friend"),
]
