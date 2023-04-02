from rest_framework import filters, viewsets, permissions
from django_filters.rest_framework import (DjangoFilterBackend, FilterSet,
                                           CharFilter)

from reviews.models import Title, Category, Genre
from .permissions import IsSafeOrReadOnly
from .serializers import (TitleSerializerGet, TitleSerializerPost,
                          CategorySerializer, GenreSerializer)


class CategoryFilter(FilterSet):
    category = CharFilter(field_name="category__slug")
    genre = CharFilter(field_name="genre__slug")

    class Meta:
        model = Title
        fields = ['name', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsSafeOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    filterset_class = CategoryFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    def get_serializer_class(self):
        actions = ['list', 'delete', 'retrieve']
        if self.action in actions:
            return TitleSerializerGet
        else:
            return TitleSerializerPost


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsSafeOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    lookup_field = 'slug'
    search_fields = ('name',)
    filter_backends = (filters.SearchFilter,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsSafeOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    lookup_field = 'slug'
    search_fields = ('name',)
    filter_backends = (filters.SearchFilter,)
