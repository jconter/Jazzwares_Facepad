from content.models import Content
from content.serializers import ContentSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class CreateContentView(generics.ListCreateAPIView):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        self.queryset = Content.objects.filter(owner=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
