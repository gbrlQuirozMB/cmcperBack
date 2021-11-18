from rest_framework import serializers
from .models import *


class ComunicadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comunicado
        fields = '__all__'


class ComunicadoFilteredListSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(source='get_categoria_display')

    class Meta:
        model = Comunicado
        fields = '__all__'
