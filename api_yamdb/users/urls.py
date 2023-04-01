from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import UserViewSet, UserMeViewSet, SignupView, TokenView

app_name = "users"

router = DefaultRouter()
router.register(r"users/me", UserMeViewSet, basename='users')
router.register(r"users", UserViewSet, basename='users')

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', TokenView.as_view(), name='token'),
    #path("users/me/", UserMeViewSet.as_view({'get': 'retrieve',
                                          #   'patch': 'partial_update'}),
      #   name='me'),
    path("", include(router.urls)),
]
