from uuid import uuid4
from django.db import models


class RoleModel(models.Model):
    id = models.UUIDField(default=uuid4, editable=False, unique=True, primary_key=True)
    role_name = models.CharField(max_length=2000, unique=True)
    datetime_created = models.DateField(auto_now_add=True, null=True)
