from uuid import uuid4
from django.db import models
from roles.models import RoleModel
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    id = models.UUIDField(default=uuid4, editable=False, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(unique=True, max_length=125)
    role = models.ForeignKey(RoleModel, on_delete=models.CASCADE)
    datetime_created = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'username'
