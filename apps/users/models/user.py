from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.default.models.base_model import BaseModel


class User(AbstractUser, BaseModel):
    username = None
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(
        verbose_name='email address',
        unique=True,
        max_length=255
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.email}'

    def save(self, *args, **kwargs):
        print(f"Guardando contraseña: {self.password}")
        return super().save(*args, **kwargs)
