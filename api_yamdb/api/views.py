from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Title, Category, Genre
from .permissions import IsSafeOrReadOnly
from .serializers import (TitleSerializer, CategorySerializer, GenreSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = (IsSafeOrReadOnly,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsSafeOrReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (IsSafeOrReadOnly,)
