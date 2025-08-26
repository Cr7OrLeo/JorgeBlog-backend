from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    def create(self, request, *args, **kwargs):
        print(request.FILES)  # Debug line
        return super().create(request, *args, **kwargs)