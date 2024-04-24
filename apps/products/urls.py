from django.urls import include, path
from rest_framework import routers

from apps.products.views.product_view import ProductViewSet

router = routers.DefaultRouter()

router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
