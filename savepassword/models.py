from uuid import uuid4
from django.db import models
from users.models import Users


class SavePasswordModel(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, unique=True, primary_key=True)
    site = models.CharField(max_length=2000)
    username = models.CharField(max_length=2000)
    password = models.CharField(max_length=2000)

    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    datetime_created = models.DateField(auto_now_add=True)
    datetime_updated = models.DateField(auto_now=True)
