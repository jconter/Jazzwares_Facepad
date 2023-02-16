from django.urls import path

from .views import CreateContentView

app_name = "content"

urlpatterns = [
    path("content/create/", CreateContentView.as_view(), name="content"),
]
