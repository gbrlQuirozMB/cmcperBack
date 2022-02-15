from rest_framework import fields, serializers
from .models import *

from django.contrib.auth.models import Permission, User


class PermisosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'