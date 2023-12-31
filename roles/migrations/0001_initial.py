# Generated by Django 4.2.2 on 2023-06-15 06:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RoleModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('role_name', models.CharField(max_length=2000)),
                ('datetime_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
