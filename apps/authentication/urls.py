from django.urls import include, path

from rest_framework import routers

from apps.authentication.views.auth_view import AuthenticationViewSet
from rest_framework_simplejwt.views import TokenRefreshView
router = routers.DefaultRouter()

router.register(r'authentication', AuthenticationViewSet, basename='authentication')

urlpatterns = [
    path('', include(router.urls)),
    path('authentication/refresh_token/',
         TokenRefreshView.as_view(), name='token_refresh'),
]
