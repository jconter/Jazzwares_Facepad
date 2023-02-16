from content.models import Comment, Content, Rating
from rest_framework import serializers


class ContentSerializer(serializers.ModelSerializer):
    """Serializer for handling the Content Model"""

    class Meta:
        model = Content
        fields = ("media", "title", "description", "owner", "created_date")
        read_only_fields = ("created_date", "owner")


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for handling the Comment Model"""

    class Meta:
        model = Comment
        fields = ("id", "owner", "content", "text", "created_date", "parent_comment")
        read_only_fields = ("id", "created_date", "owner", "content", "parent_comment")


class RatingSerializer(serializers.ModelSerializer):
    """Serializer for handling the Rating Model"""

    value = serializers.IntegerField(max_value=5, min_value=1)

    class Meta:
        model = Rating
        fields = ("owner", "content", "value", "created_date")
        read_only_fields = ("owner", "content", "created_date")
