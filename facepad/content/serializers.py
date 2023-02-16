from content.models import Content
from rest_framework import serializers


class ContentSerializer(serializers.ModelSerializer):
    """Serializer for handling the Content Model"""

    class Meta:
        model = Content
        fields = ("media", "title", "description", "owner", "created_date")
        read_only_fields = ("created_date", "owner")
