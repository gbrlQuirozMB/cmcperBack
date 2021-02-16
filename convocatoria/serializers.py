from preregistro.models import Medico
from .models import *
from rest_framework import serializers


class EsExtranjeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'isExtranjero', 'nacionalidad']


class EstudioExtranjeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'estudioExtranjero', 'escuelaExtranjero']


class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = ['descripcion']


class ConvocatoriaSerializer(serializers.ModelSerializer):
    sedes = SedeSerializer(required=False, many=True)
    tipoExamenes = SedeSerializer(required=False, many=True)

    class Meta:
        model = Convocatoria
        # evito poner todo el listado de campos
        fields = [f.name for f in model._meta.fields] + ['sedes'] + ['tipoExamenes']

    def create(self, validated_data):
        sedesData = validated_data.pop('sedes')
        tipoExamenesData = validated_data.pop('tipoExamenes')
        convocatoria = Convocatoria.objects.create(**validated_data)
        for sedeData in sedesData:
            Sede.objects.create(**sedeData, convocatoria=convocatoria)
        for tipoExameneData in tipoExamenesData:
            TipoExamen.objects.create(**tipoExameneData, convocatoria=convocatoria)
        # return validated_data # incompleto porque ya se le quito la llave 'sedes'
        return convocatoria


class ConvocatoriaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convocatoria
        fields = ['id', 'nombre']


class ConvocatoriaGetDetailSerializer(serializers.ModelSerializer):
    sedes = SedeSerializer(read_only=True, many=True)
    tipoExamenes = SedeSerializer(read_only=True, required=False, many=True)

    class Meta:
        model = Convocatoria
        fields = [f.name for f in model._meta.fields] + ['sedes'] + ['tipoExamenes']
        