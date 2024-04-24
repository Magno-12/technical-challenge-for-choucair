from django.test import Client, TransactionTestCase
from rest_framework import status

from apps.users.models.user import User


class AuthenticationViewSetTest(TransactionTestCase):
    def setUp(self):
        """
        Set up the test environment by creating a user for testing.
        """
        self.client = Client()
        self.user_data = {
            "username": None,
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

    def login_and_get_token(self):
        """
        Perform a login and return the access token for use in other tests.
        """
        login_url = '/authentication/login/'
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(
            login_url,
            data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK, response.data)
        return response.data['access']

    def test_successful_login(self):
        """
        Test a successful login.
        """
        token = self.login_and_get_token()
        self.assertTrue(token)

    def test_successful_logout(self):
        """
        Test an successful logout.
        """
        token = self.login_and_get_token()
        logout_url = '/authentication/logout/'
        headers = {'Authorization': f'Bearer {token}'}
        data = {'refresh_token': token}
        response = self.client.post(
            logout_url,
            data=data,
            content_type='application/json',
            **headers
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsuccessful_login(self):
        """
        Test an successful login.
        """
        login_url = '/authentication/login/'
        data = {
            "email": self.user_data["email"],
            "password": "wrongpassword",
        }
        response = self.client.post(
            login_url,
            data,
            content_type='application/json'
        )
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED, response.data)
