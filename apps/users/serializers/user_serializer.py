from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from apps.users.models.user import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'email'
                ]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password'
        ]

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        password = validated_data.get('password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password
        user = super(UserCreateSerializer, self).create(validated_data)
        return user
