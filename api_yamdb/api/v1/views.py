from django_filters.rest_framework import (
    CharFilter, DjangoFilterBackend, FilterSet,
)
from rest_framework import filters, mixins, status, viewsets
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genre, Review, Title
from users.models import User

from .permissions import (
    IsAdmin, IsAdminModeratorAuthorOrReadOnly, IsAdminOrRead,
)
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer, ReviewSerializer,
    SignupSerializer, TitleSerializerGet, TitleSerializerPost, TokenSerializer,
    UserMeSerializer, UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    serializer_class = UserSerializer
    queryset = User.objects.all()
    http_method_names = ["get", "patch", "post", "delete"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        data = serializer.data
        return Response(
            data,
            status=status.HTTP_201_CREATED,
        )


class MeView(RetrieveUpdateAPIView):
    serializer_class = UserMeSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "patch"]

    def get_object(self):
        return self.request.user


class SignupView(CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        email = request.data.get("email")
        username = request.data.get("username")
        user = User.objects.filter(username=username, email=email).exists()
        if serializer.is_valid() or user:
            user, created = User.objects.get_or_create(
                username=username, email=email
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                "Confirm your registration",
                f"Your confirmation code is: {confirmation_code}",
                None,
                [email],
                fail_silently=False,
            )
            return Response(
                {"email": email, "username": username},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(CreateAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        confirmation_code = request.data.get("confirmation_code")
        username = request.data.get("username")
        if not username or not confirmation_code:
            return Response(
                {"error": "Username and confirmation code are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not User.objects.filter(username=username).exists():
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if serializer.is_valid():
            user = User.objects.get(username=username)
            if default_token_generator.check_token(user, confirmation_code):
                token = RefreshToken.for_user(user)
                return Response(
                    {"token": str(token.access_token)},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid confirmation code"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    queryset = (
        Title.objects.select_related("category")
        .prefetch_related("genre")
        .annotate(rating_avg=Avg("reviews__score"))
    )
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
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.select_related("author")

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        return review.comments.select_related("author")

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)
