from rest_framework import generics
from rest_framework import viewsets


from blog.models import Post
from blog.models import Tag

from blog.api.permissions import AuthorModifyOrReadOnly
from rest_framework.permissions import IsAdminUser
from blog.api.permissions import IsAdminUserForObject

from blango_auth.models import User

from blog.api.serializers import PostSerializer
from blog.api.serializers import UserSerializer
from blog.api.serializers import PostDetailSerializer
from blog.api.serializers import TagSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

# class PostList(generics.ListCreateAPIView):
#   queryset = Post.objects.all()
#   serializer_class = PostSerializer


# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#   queryset = Post.objects.all()
#   serializer_class = PostSerializer

# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#   # permissions_classes = [AuthorModifyOrReadOnly]
#   # permissions_classes = [AuthorModifyOrReadOnly | IsAdminUser]
#   permissions_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
#   queryset = Post.objects.all()
#   # serializer_class = PostSerializer
#   serializer_class = PostDetailSerializer

class UserDetail(generics.RetrieveAPIView):
  lookup_field = "email"
  queryset = User.objects.all()
  serializer_class = UserSerializer

class TagViewSet(viewsets.ModelViewSet):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer

  @action(methods=['get'], detail=True, name="Posts with the Tag")
  def posts(self, request, pk=None):
    tag = self.get_object()
    post_serializer = PostSerializer(
        tag.posts, many=True, context={"request": request}
    )
    return Response(post_serializer.data)

class PostViewSet(viewsets.ModelViewSet):
  permissions_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
  queryset = Post.objects.all()

  def get_serializer_class(self):
    if self.action in ("list", "create"):
      return PostSerializer
    return PostDetailSerializer