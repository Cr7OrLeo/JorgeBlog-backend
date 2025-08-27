from urllib import request
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from rest_framework.parsers import MultiPartParser, FormParser

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)

    # Pass the request to the serializer context so build_absolute_uri works
    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        print("FILES:", request.FILES)  # should show your uploaded file
        print("DATA:", request.data)     # form data
        return super().create(request, *args, **kwargs)
