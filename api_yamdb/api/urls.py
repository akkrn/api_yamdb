from rest_framework import routers

from django.urls import include, path

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = routers.DefaultRouter()
router.register("titles", TitleViewSet, basename="title")
router.register("categories", CategoryViewSet, basename="category")
router.register("genres", GenreViewSet, basename="genre")

urlpatterns = [
    path("", include(router.urls)),
]
