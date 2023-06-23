# Generated by Django 4.2.2 on 2023-06-15 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('roles', '0003_alter_rolemodel_datetime_created'),
        ('users', '0002_alter_users_datetime_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='datetime_created',
            field=models.DateField(auto_now_add=True, default='2023-6-15'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='users',
            name='role',
            field=models.ForeignKey(default='53704371-2a36-453f-a8e5-57b0b6aae310', on_delete=django.db.models.deletion.CASCADE, to='roles.rolemodel'),
            preserve_default=False,
        ),
    ]