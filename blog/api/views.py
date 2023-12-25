from rest_framework import generics 

from blog.api.serializers import PostSerializer
from blog.models import Post 

from blog.api.permissions import AuthorModifyOrReadOnly
from rest_framework.permissions import IsAdminUser
from blog.api.permissions import IsAdminUserForObject

class PostList(generics.ListCreateAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer


# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#   queryset = Post.objects.all()
#   serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
  # permissions_classes = [AuthorModifyOrReadOnly]
  # permissions_classes = [AuthorModifyOrReadOnly | IsAdminUser]
  permissions_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
  queryset = Post.objects.all()
  serializer_class = PostSerializer