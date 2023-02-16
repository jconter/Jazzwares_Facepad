from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import FriendRequestResponse, GetFriendRequests, RegisterView, RequestFriend,GetUserView, RegisterView

app_name = "users"

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/token-refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('user/<username>/', GetUserView.as_view(), name='get_user'),
    path("friends/friend-request/", RequestFriend.as_view(), name="request_friend"),
    path("friends/requests/", GetFriendRequests.as_view(), name="get_friend_requests"),
    path(
        "friends/request/response/<int:pk>",
        FriendRequestResponse.as_view(),
        name="respond_to_friend_request",
    ),
]
