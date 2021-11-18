from api.exceptions import *
from .models import *
from rest_framework import fields, serializers
# from api.logger import log
import logging
log = logging.getLogger('django')


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


class CatEntidadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatEntidad
        fields = '__all__'


class CatSedesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatSedes
        fields = '__all__'
