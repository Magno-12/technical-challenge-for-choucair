from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from rest_framework import routers

from apps.products.views.product_view import ProductViewSet

router = routers.DefaultRouter()

router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
