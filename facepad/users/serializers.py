from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import FriendRequest


class UserSerializer(serializers.ModelSerializer):
    """Serializer for handling the User Model"""

    class Meta:
        model = get_user_model()
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
            "date_of_birth",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = get_user_model().objects.create(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"],
            username=validated_data["username"],
            date_of_birth=validated_data["date_of_birth"],
            user_type="regular",
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class FriendRequestSerializer(serializers.ModelSerializer):
    """Serializer for handling the FriendRequest model"""

    requestee = serializers.SlugRelatedField(
        slug_field="username",
        queryset=get_user_model().objects.all(),
    )
    requestor = serializers.SlugRelatedField(
        slug_field="username", queryset=get_user_model().objects.all(), allow_null=True
    )

    class Meta:
        model = FriendRequest
        fields = ["id", "requestor", "requestee", "status", "created_date"]
        read_only_fields = ["id", "created_date"]
