import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TransactionTestCase
from django.conf import settings

from rest_framework import status

from apps.products.models.product import Product
from apps.users.models.user import User


class ProductViewSetTest(TransactionTestCase):
    def setUp(self):
        """
        Set up the test environment by creating a user and a product for testing.
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
        self.token = self.login_and_get_token()
        self.product_data = {
            "name": "Test Product",
            "description": "Test Description",
            "price": 10.0,
            "stock": 20,
            "image": "test_image.jpg",
            "user": self.user
        }
        self.product = Product.objects.create(**self.product_data)

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

    def test_list_products(self):
        response = self.client.get('/product/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product(self):
        response = self.client.get(f'/product/{self.product.id}/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 15.0,
            "stock": 10,
        }
        response = self.client.post('/product/create_product/', data=product_data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_create_product_with_image(self):
        test_image_path = os.path.join(settings.MEDIA_ROOT, 'product_image', 'IMG_20220708_094204.jpg') #en esta linea cambiar el nombre de la imagen
        with open(test_image_path, 'rb') as image_file:
            image_content = image_file.read()
        image_file = SimpleUploadedFile('IMG_20220708_094204.jpg', image_content, content_type='image/jpeg') #en esta linea cambiar el nombre de la imagen

        product_data = {
            "name": "New Product",
            "description": "New Description",
            "price": 15.0,
            "stock": 10,
            "image": image_file,
        }

        response = self.client.post('/product/create_product/', data=product_data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_partial_update_product(self):
        updated_data = {
            "price": 20.0,
        }
        response = self.client.patch(f'/product/{self.product.id}/', data=updated_data, content_type='application/json', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        response = self.client.delete(f'/product/{self.product.id}/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_buy_product(self):
        initial_stock = self.product.stock
        response = self.client.post(f'/product/{self.product.id}/buy/', HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "Product purchased")
        self.assertEqual(response.data['remaining_stock'], initial_stock - 1)
