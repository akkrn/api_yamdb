from rest_framework.routers import DefaultRouter

from django.urls import include, path

app_name = "users"

router = DefaultRouter()

router.register(
    r"posts/(?P<post_id>\d+)/comments", ..., basename="comments")

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
]
