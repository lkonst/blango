from django_filters import rest_framework as filters
from blog.models import Post


class PostFilterSet(filters.FilterSet):
  published_from = filters.DateFilter(
      field_name = "publish_at", lookup_expr="gte", label="Published Date From")
  
  published_to = filters.DateFilter(
      field_name = "publish_at", lookup_expr="lte", label="Publish Date To")
  
  author_email = filters.CharFilter(
    field_name = "author_email",
    lookup_expr = "icontains",
    label = "Author Email Contains",)

  summary = filters.CharFilter(
      field_name = "summary",
      lookup_expr = "icontains",
      label = "Summary Contains",)
  
  content = filters.CharFilter(
      field_name = "content",
      lookup_expr = "icontains",
      label = "Content Contains",)

  class Meta:
    model = Post
    fields = ["author", "tags"]