from rest_framework import fields, serializers
from .models import *


class CertificadosFilteredListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['nombreCompleto'] = instance.medico.nombre + ' ' + instance.medico.apPaterno

        return repr


class CertificadoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = ['id', 'documento']
