from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend


from reviews.models import Title, Category, Genre
from .permissions import IsSafeOrReadOnly
from .serializers import (TitleSerializer, CategorySerializer, GenreSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    # permission_classes = (IsSafeOrReadOnly,)
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsSafeOrReadOnly,)
    lookup_field = 'slug'
    search_fields = ('name',)
    filter_backends = (filters.SearchFilter,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (IsSafeOrReadOnly,)
    lookup_field = 'slug'
    search_fields = ('name',)
    filter_backends = (filters.SearchFilter,)
