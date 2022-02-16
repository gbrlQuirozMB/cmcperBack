from rest_framework import fields, serializers
from .models import *

from django.contrib.auth.models import Permission, User


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
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']


class UsuariosUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
