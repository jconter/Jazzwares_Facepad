from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import GetUserView, RegisterView

app_name='users'

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/<username>/', GetUserView.as_view(), name='get_user')
]
