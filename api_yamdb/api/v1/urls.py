from rest_framework.routers import DefaultRouter

from django.urls import include, path

from users.views import MeView, SignupView, TokenView, UserViewSet

from .views import (
    CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, TitleViewSet,
)

app_name = "api"

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GenreViewSet, basename="genres")
router.register("titles", TitleViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router.register(r"users", UserViewSet, basename="users")


urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/token/", TokenView.as_view(), name="token"),
    path("users/me/", MeView.as_view(), name="user_detail"),
    path("", include(router.urls)),
]
