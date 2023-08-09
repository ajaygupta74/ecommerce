from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone_number = PhoneNumberField(null=True, unique=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    gender = models.BooleanField(null=True)

    groups = models.ManyToManyField(
        Group, related_name='custom_users')

    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_users')
