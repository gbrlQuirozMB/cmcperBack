from rest_framework import fields, serializers
from .models import *

from django.contrib.auth.models import Permission, User


class PermisosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class UsuariosFilteredListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UsuariosDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'user_permissions']
