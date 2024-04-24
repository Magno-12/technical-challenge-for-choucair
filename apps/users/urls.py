from django.urls import include, path
from rest_framework import routers

from apps.users.views.user_view import UserViewSet

router = routers.DefaultRouter()

router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
