from rest_framework import fields, serializers
from .models import *
from certificados.models import Certificado


class MedicosListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = ['id']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['nombreDiploma'] = instance.medico.diplomaConacem
        repr['numCertificado'] = instance.medico.numRegistro

        return repr
