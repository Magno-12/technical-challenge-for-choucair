from django.db import models

from apps.default.models.base_model import BaseModel
from apps.users.models.user import User


class Product(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='product_image/')

    def __str__(self):
        return self.name
