from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.users.models.user import User
from apps.users.serializers.user_serializer import (
    UserCreateSerializer,
    UserSerializer
)


class UserViewSet(GenericViewSet):
    queryset = User.objects.filter(is_active=True)

    def get_permission_classes(self):
        if self.action == 'create_user':
            return [AllowAny]
        else:
            return [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create_user':
            return UserCreateSerializer
        else:
            return UserSerializer

    def get_object(self, pk):
        try:
            return self.queryset.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound(detail="Object not found")

    def list(self, request):
        """
        List all users.

        ---
        response:
            Response: Serialized data of all users.
            Example JSON:
            {
                "data": [
                    {
                        "id": "str",
                        "email": "str",
                    },
                    ...
                ]
            }
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def create_user(self, request):
        """
        Creates a new user.

        Takes first name, last name, email, and password as input.

        ---
        Body:
            {
                "first_name": "str",
                "last_name": "str",
                "email": "str",
                "password": "str"
            }

        responses:
            {
                "id": "user_id",
                "first_name": "first_name",
                "last_name": "last_name",
                "email": "email"
            }
        """
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        """
        Partially updates a user.

        Takes first name, last name, and/or email as input.

        ---
        Body:
            {
                "first_name": "str",
                "last_name": "str",
                "email": "str"
            }

        responses:
            {
                "id": "user_id",
                "first_name": "first_name",
                "last_name": "last_name",
                "email": "email"
            }
        """
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        """
        Deletes a user.

        responses:
            {
                "detail": "User deleted successfully"
            }
        """
        user = self.get_object(pk)
        user.delete()

        return Response({"detail": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
