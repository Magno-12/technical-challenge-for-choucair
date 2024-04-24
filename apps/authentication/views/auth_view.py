from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


from apps.users.models.user import User
from apps.authentication.serializers.authentication_serializer import (
    AuthenticationSerializer,
    LogoutSerializer,
)


class AuthenticationViewSet(GenericViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'login':
            return AuthenticationSerializer
        else:
            return LogoutSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Logs in an existing user using their email and password.

        Takes email and password as input.

        If the provided email and password are correct,
        returns a new refresh and access token for the user.
        The refresh token can be used to generate new access tokens.
        ---
        Body:
            {
                "email": "str",
                "password": "str"
            }

        responses:
            {
                "refresh": "refresh_token",
                "access": "access_token",
                "user": {
                    "id": "user_id",
                    "email": "email",
                }
            }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data

        print(f"Datos validados por AuthenticationSerializer: {user_data}")
        print(f"Contraseña proporcionada: {user_data.get('password')}")

        try:
            user = User.objects.get(email=user_data['email'])
        except User.DoesNotExist:
            raise AuthenticationFailed(
                "User with the provided email does not exist")

        print(f"Contraseña proporcionada: {user_data['password']}")

        # Mensaje de depuración para verificar el usuario recuperado
        print(f"Usuario recuperado de la base de datos: {user}")

        # Mensaje de depuración para verificar la contraseña almacenada
        print(f"Contraseña almacenada: {user.password}")

        # Verifica que la contraseña proporcionada coincida con la almacenada
        if not check_password(user_data['password'], user.password):
            raise AuthenticationFailed("Incorrect password")

        # Mensaje de depuración para verificar que la contraseña coincidió
        print("Contraseña coincidió correctamente.")

        refresh = RefreshToken.for_user(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Logs out the current user.

        If the user is logged in,
        deletes their refresh token.
        This prevents them from generating new access tokens.

        responses:
            {
                "detail": "Successfully logged out"
            }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = request.data.get('refresh')

        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except RefreshToken.InvalidToken:
                logout(request)
                return Response({"detail": "Refresh token is invalid"},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Successfully logged out"},
                        status=status.HTTP_200_OK)
