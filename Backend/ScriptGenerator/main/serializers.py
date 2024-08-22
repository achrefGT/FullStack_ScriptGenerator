from django.contrib.auth.models import User
from rest_framework import serializers # type: ignore
from .models import Script

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user

class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ["id", "content", "created_at", "user"]
        extra_kwargs = {"user": {"read_only": True}}
