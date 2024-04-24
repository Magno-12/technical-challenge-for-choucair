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
        print(f"Contraseña sin hashear: {password}")
        hashed_password = make_password(password)
        print(f"Contraseña hasheada: {hashed_password}")
        validated_data['password'] = hashed_password
        print(f"Datos validados antes de crear usuario: {validated_data}")
        user = super(UserCreateSerializer, self).create(validated_data)
        print(f"Contraseña guardada en la base de datos: {user.password}")
        return user
