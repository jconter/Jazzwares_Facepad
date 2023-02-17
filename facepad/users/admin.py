from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm
from .models import FriendRequest, User


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    fieldsets = UserAdmin.fieldsets + (  # type: ignore
        ("Profile", {"fields": ("user_type", "date_of_birth", "friends")}),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(FriendRequest)
