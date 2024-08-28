from django.contrib.auth.models import User
from rest_framework import serializers # type: ignore
from .models import LowLevelDesign, RadioSite, Router, Script, StaticRoute

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user

class RadioSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadioSite
        fields = ["id", "name", "lld"]

class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = ["id", "content", "created_at"]

class StaticRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticRoute
        fields = ['id', 'destination', 'next_hop']

class RouterSerializer(serializers.ModelSerializer):
    o_and_m_route = StaticRouteSerializer(read_only=True)
    tdd_route = StaticRouteSerializer(read_only=True)

    class Meta:
        model = Router
        fields = ['id', 'name', 'o_and_m_route', 'tdd_route']

class LowLevelDesignSerializer(serializers.ModelSerializer):
    routers = RouterSerializer(many=True, read_only=True)

    class Meta:
        model = LowLevelDesign
        fields = ['id', 'file', 'created_at', 'routers', 'radio_sites']  

