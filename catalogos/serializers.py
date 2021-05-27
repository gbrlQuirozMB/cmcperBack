from .models import *
from rest_framework import fields, serializers
from api.logger import log
from api.exceptions import *


class CatMotivosRechazoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatMotivosRechazo
        fields = '__all__'


class CatMotivosRechazoFilteredSerializer(serializers.ModelSerializer):
    tipo = serializers.CharField(source='get_tipo_display')

    class Meta:
        model = CatMotivosRechazo
        fields = '__all__'


class CatPagosSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatPagos
        fields = ['id', 'precio']


class CatPagosFilteredListSerializer(serializers.ModelSerializer):
    # tipo = serializers.CharField(source='get_tipo_display')

    class Meta:
        model = CatPagos
        fields = '__all__'
