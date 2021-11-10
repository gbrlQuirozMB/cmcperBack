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

class DetalleConcacemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleConcacem
        fields = ['medico']


class ConacemSerializer(serializers.ModelSerializer):
    medicos = DetalleConcacemSerializer(required=False, many=True)

    class Meta:
        model = Conacem
        # fields = '__all__'
        fields = [f.name for f in model._meta.fields] + ['medicos']

    def create(self, validated_data):
        if validated_data.get('medicos') is None:
            conacem = Conacem.objects.create(**validated_data)
            return conacem

        medicosData = validated_data.pop('medicos')
        conacem = Conacem.objects.create(**validated_data)
        for medicoData in medicosData:
            DetalleConcacem.objects.create(**medicoData, conacem=conacem)
        return conacem
