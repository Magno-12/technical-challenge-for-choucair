from django.test import Client, TransactionTestCase
from rest_framework import status

from apps.users.models.user import User


class UserViewSetTest(TransactionTestCase):
    def setUp(self):
        """
        Set up the test environment by creating a user for testing.
        """
        self.client = Client()
        self.user_data = {
            "first_name": "Kirby",
            "last_name": "Fox",
            "email": "test@example.com",
            "password": "testpassword",
        }
        self.user = User.objects.create_user(
            email=self.user_data["email"],
            password=self.user_data["password"],
            first_name=self.user_data["first_name"],
            last_name=self.user_data["last_name"]
        )

    def test_list_users(self):
        """
        Test listing all users.
        """
        response = self.client.get('/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificar que los datos de los usuarios son correctos
        self.assertGreater(len(response.data), 0)
        # Verificar que se devuelven los campos esperados
        self.assertIn('id', response.data[0])
        self.assertIn('email', response.data[0])

    def test_create_user(self):
        """
        Test creating a new user.
        """
        new_user_data = {
            "first_name": "link",
            "last_name": "zelda",
            "email": "zeldatotk@test.com",
            "password": "newpassword",
        }
        response = self.client.post('/user/create_user/', data=new_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['first_name'], new_user_data['first_name'])
        self.assertEqual(response.data['last_name'], new_user_data['last_name'])
        self.assertEqual(response.data['email'], new_user_data['email'])

    def test_partial_update_user(self):
        """
        Test partially updating a user.
        """
        updated_data = {
            "first_name": "Updated",
            "last_name": "Name",
        }
        response = self.client.patch(f'/user/{self.user.id}/', data=updated_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], updated_data['first_name'])
        self.assertEqual(response.data['last_name'], updated_data['last_name'])

    def test_delete_user(self):
        """
        Test deleting a user.
        """
        response = self.client.delete(f'/user/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(pk=self.user.id)
