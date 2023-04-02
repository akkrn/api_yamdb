from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import MeView, SignupView, TokenView, UserViewSet

app_name = "users"

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/token/", TokenView.as_view(), name="token"),
    path("users/me/", MeView.as_view(), name="user_detail"),
    path("", include(router.urls)),
]
