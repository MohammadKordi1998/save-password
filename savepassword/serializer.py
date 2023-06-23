from rest_framework import serializers
from rest_framework.serializers import Serializer


class SPasswordSerializer(Serializer):
    site = serializers.CharField(max_length=2000)
    username = serializers.CharField(max_length=2000)
    is_random_pass = serializers.BooleanField()
    password: serializers.CharField(max_length=2000)

    password_len = serializers.CharField(max_length=10)
    user_id = serializers.UUIDField()
