from rest_framework import serializers
from .models import *


class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = '__all__'


class InstitucionFilteredListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = ['id', 'nombreInstitucion', 'rfc', 'contacto', 'email', 'telUno']
