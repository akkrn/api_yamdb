from django_filters.rest_framework import (
    CharFilter,
    DjangoFilterBackend,
    FilterSet,
)
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from reviews.models import Category, Genre, Title
from users.permissions import IsAdminOrRead

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializerGet,
    TitleSerializerPost,
)


class ListCreateDeleteView(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    pass


class CategoryFilter(FilterSet):
    category = CharFilter(field_name="category__slug")
    genre = CharFilter(field_name="genre__slug")

    class Meta:
        model = Title
        fields = ["name", "year"]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filterset_class = CategoryFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    permission_classes = (IsAdminOrRead,)

    def get_serializer_class(self):
        actions = ["list", "delete", "retrieve"]
        if self.action in actions:
            return TitleSerializerGet
        else:
            return TitleSerializerPost

class CategoryViewSet(ListCreateDeleteView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    search_fields = ("name",)
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrRead,)

class GenreViewSet(ListCreateDeleteView):
    queryset = Genre.objects.all()
    lookup_field = "slug"
    search_fields = ("name",)
    filter_backends = (filters.SearchFilter,)
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrRead,)
