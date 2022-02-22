from rest_framework import fields, serializers
from .models import *

from django.contrib.auth.models import Permission, User
from django.contrib.auth.hashers import make_password


class PermisosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['app_label'] = instance.content_type.app_label

        return repr


class UsuariosFilteredListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UsuariosDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'user_permissions']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['codenames'] = instance.get_user_permissions()

        return repr


class UsuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_staff']

    def create(self, validated_data):
        self.clave = validated_data['password']
        validated_data['password'] = make_password(validated_data['password'])
        # return User(**validated_data)
        return User.objects.create(**validated_data)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['pass_plain'] = self.clave

        return repr


class UsuariosUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
