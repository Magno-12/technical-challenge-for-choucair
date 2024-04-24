from rest_framework import serializers

from apps.products.models.product import Product
from apps.users.models.user import User


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Product
        fields = ['id',
                  'user',
                  'name',
                  'description',
                  'price',
                  'stock',
                  'image'
                ]
        extra_kwargs = {
            'image': {'required': False}
        }

    def create(self, validated_data):
        """
        Create a new product instance.
        Ensures that the product is associated with the user making the request.
        """
        user = self.context['request'].user
        validated_data['user'] = user
        return super(ProductSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing product instance.

        Ensures that only allowed fields can be updated by removing any key
        that shouldn't be updated by the user after the initial create.
        """
        for field in ['user', 'id']:
            validated_data.pop(field, None)

        return super(ProductSerializer, self).update(instance, validated_data)
