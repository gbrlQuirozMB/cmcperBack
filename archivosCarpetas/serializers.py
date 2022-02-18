from rest_framework import serializers
from .models import *


class CarpetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carpeta
        fields = '__all__'


class CarpetaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carpeta
        fields = '__all__'


class CarpetaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carpeta
        fields = '__all__'


# --------------------------ARCHIVOS--------------------------

class ArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archivo
        fields = '__all__'


class ArchivoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archivo
        fields = '__all__'


class ArchivoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Archivo
        fields = '__all__'
