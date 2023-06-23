from rest_framework import serializers
from rest_framework.serializers import Serializer


class UserSerializer(Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=125)
    role_id = serializers.UUIDField()
    password = serializers.CharField(max_length=100)
