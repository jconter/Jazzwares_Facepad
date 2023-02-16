from content.models import Comment, Content
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
        fields = ("owner", "content", "text", "created_date", "parent_comment")
        read_only_fields = ("created_date", "owner")
