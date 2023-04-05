from django_filters.rest_framework import (
    CharFilter,
    DjangoFilterBackend,
    FilterSet,
)
from rest_framework import filters, mixins, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from rest_framework import permissions

from reviews.models import Category, Genre, Review, Title
from users.permissions import IsAdminOrRead
from .permissions import (IsAdminModeratorAuthorOrReadOnly)

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializerGet,
    TitleSerializerPost,
    CommentSerializer,
    ReviewSerializer
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


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminModeratorAuthorOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAdminModeratorAuthorOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        serializer.save(
            author=self.request.user,
            review=review
        )
