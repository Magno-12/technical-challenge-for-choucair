from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.products.models.product import Product
from apps.products.serializers.product_serializer import ProductSerializer


class ProductViewSet(GenericViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.filter(is_active=True)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'buy']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        return ProductSerializer

    def list(self, request):
        """
        List all products.

        ---
        response:
            200 OK: Serialized data of all products.
            Example JSON:
                [
                    {
                        "id": "str",
                        "name": "str",
                        "description": "str",
                        "price": "float",
                        "stock": "int",
                        "image": "url",
                        "user": "user_id"
                    },
                    ...
                ]
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Retrieve a specific product by its ID.

        ---
        response:
            200 OK: Serialized data of a specific product.
            Example JSON:
                {
                    "id": "str",
                    "name": "str",
                    "description": "str",
                    "price": "float",
                    "stock": "int",
                    "image": "url",
                    "user": "user_id"
                }
        """
        product = self.get_object_or_404(pk=pk)
        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def create_product(self, request):
        """
        Creates a new product instance.

        ---
        Body:
            {
                "name": "str",
                "description": "str",
                "price": "float",
                "stock": "int",
                "image": "upload"  // Use the correct form data key for image uploads.
            }

        responses:
            201 Created: Product successfully created.
            Example JSON:
                {
                    "id": "str",
                    "name": "str",
                    "description": "str",
                    "price": "float",
                    "stock": "int",
                    "image": "url",
                    "user": "user_id"
                }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        """
        Updates a specific product by its ID.

        ---
        Body:
            {
                "name": "str",
                "description": "str",
                "price": "float",
                "stock": "int",
                "image": "upload"
            }

        responses:
            200 OK: Product successfully updated.
            403 Forbidden: Not allowed to update this product.
        """
        product = self.get_object()
        if request.user != product.user:
            raise PermissionDenied("You do not have permission to update this product.")
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """
        Deletes a specific product by its ID.

        Only the user who created the product can perform this action.

        ---
        responses:
            204 No Content: Product successfully deleted.
            403 Forbidden: User does not have permission to delete this product.
            404 Not Found: Product not found.
        """
        product = self.get_object_or_404(pk=pk)
        if request.user != product.user:
            return Response({"detail": "You do not have permission to delete this product."},
                status=status.HTTP_403_FORBIDDEN
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def buy(self, request, pk=None):
        """
        Buys a specific product by decreasing its stock by 1.

        Any authenticated user can perform this action. The stock must be greater than 0.

        ---
        Body:
            No body required for this action.

        responses:
            200 OK: Product successfully purchased.
            Example JSON:
                {
                    "status": "Product purchased",
                    "remaining_stock": <int>
                }
            400 Bad Request: Product is out of stock.
            404 Not Found: Product not found.
        """
        product = self.get_object_or_404(pk=pk)
        if product.stock > 0:
            product.stock -= 1
            product.save()
            return Response({"status": "Product purchased", "remaining_stock": product.stock},
                status=status.HTTP_200_OK
            )
        else:
            return Response({"detail": "Product is out of stock."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_object_or_404(self, pk):
        """
        Helper method to get the object with the provided pk or raise a 404 error if it doesn't exist.
        """
        try:
            return self.queryset.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found.")
