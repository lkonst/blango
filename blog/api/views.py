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

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers, vary_on_cookie

from rest_framework.exceptions import PermissionDenied

from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.http import Http404

import django_filters.rest_framework
from blog.api.filters import PostFilterSet

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

  @method_decorator(cache_page(180))
  def get(self, *args, **kwargs):
    return super(UserDetail, self).get(*args, **kwargs)



class TagViewSet(viewsets.ModelViewSet):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer

  @action(methods=['get'], detail=True, name="Posts with the Tag")
  def posts(self, request, pk=None):
    tag = self.get_object()

    page = self.paginate_queryset(tag.posts)

    if page is not None:

      post_serializer = PostSerializer(
          tag.posts, many=True, context={"request": request})
      return Response(post_serializer.data)

    post_serializer = PostSerializer(
      tag.posts, many=True, context={'request': request}
    )
    return Response(post_serializer.data)

  @method_decorator(cache_page(180))
  def list(self, *args, **kwargs):
    return super(TagViewSet, self).list(*args, **kwargs)

  @method_decorator(cache_page(180))
  def retrieve(self, *args, **kwargs):
    return super(TagViewSet, self).retrieve(*args, **kwargs)



class PostViewSet(viewsets.ModelViewSet):
  permissions_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
  filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
  # filterset_fields = ['author', 'tags']
  filterset_class = PostFilterSet
  ordering_fields = ["published_at", "author", "title", "slug"]
  # we will refer to this in 'get_queryset()'
  queryset = Post.objects.all()

  def get_serializer_class(self):
    if self.action in ("list", "create"):
      return PostSerializer
    return PostDetailSerializer

  @method_decorator(cache_page(180))
  @method_decorator(vary_on_headers("Authorization"))
  @method_decorator(vary_on_cookie)
  @action(methods=['get'], detail=False, name="Posts by the logged in user")
  def mine(self, request):
    if request.user.is_anonymous:
      raise PermissionDenied("You must be logged in to see which Posts are yours")
    posts = self.get_queryset().filter(author=request.user)

    page = self.paginate_queryset(posts)

    if page is not None:
      serializer = PostSerializer(page, many=True, context={"request": request})
      return self.get_paginate_response(serializer.data)

    serializer = PostSerializer(posts, many=True, context={"request": request})
    return Response(serializer.data)

  @method_decorator(cache_page(120))
  @method_decorator(vary_on_headers("Authorization", "Cookie")) # Since the list of Posts now changes with each user, 
  def list(self, *args, **kwargs):                                # we need to make sure we add the vary_on_headers() 
    return super(PostViewSet, self).list(*args, **kwargs)           # decorator to it
  
  # queryset has been set by applying user filtering rules
  def get_queryset(self):
    if self.request.user.is_anonymous:
      # published only
      # return self.queryset.filter(published_at__lte=timezone.now())
      queryset = self.queryset.filter(published_at__lte=timezone.now())
    
    # if self.request.user.is_staff:
    elif not self.request.user.is_staff:
      #allow all
      queryset = self.queryset
      
      # return self.queryset
    else:
    #filter for own or 
    # return self.queryset.filter(
    #   Q(published_at__lte=timezone.now() | Q(author=self.request.user))
    # )
      queryset = self.queryset.filter(Q(published_at__lte=timezone.now()) | Q(author=self.request.user))

  # fetch the period name URL parameter from self.kwargs
    time_period_name = self.kwargs.get("period_name")

    if not time_period_name:
      # no further filtering required
      return queryset
    
    if time_period_name == "new":
      return queryset.filter(published_at__gte=timezone.now() - timedelta(hours=1))

    elif time_period_name == "today":
      return queryset.filter(published_at__date=timezone.now().date() )

    elif time_period_name == "week":
      return queryset.filter(published_at__gte=timezone.now() - timedelta(days=7))
    else:
      raise Http404(
        f"Time period {time_period_name} is not valid, should be "
        f"'new', 'today' or 'week'"
      )