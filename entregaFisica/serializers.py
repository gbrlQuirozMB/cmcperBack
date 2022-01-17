from rest_framework import serializers
from .models import *


class EntregaFisicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntregaFisica
        fields = '__all__'


class EntregaFisicaFilteredListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntregaFisica
        fields = '__all__'
        # fields = ['id', 'fechaEntrega', 'nombreRecibe']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['tipoDocumento'] = instance.catTiposDocumentoEntrega.descripcion

        return repr
