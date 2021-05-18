from rest_framework import serializers
from .models import *


class TemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tema
        fields = ['nombre']


class ActividadAvaladaSerializer(serializers.ModelSerializer):
    temas = TemaSerializer(required=False, many=True)

    class Meta:
        model = ActividadAvalada
        fields = ['id', 'institucion', 'item', 'nombre', 'emailContacto', 'numAsistentes', 'puntosAsignar', 'fechaInicio', 'lugar', 'solicitante', 'tipoPago', 'porcentaje', 'precio', 'descripcion',
                  'temas']

    def create(self, validated_data):
        if validated_data.get('temas') is None:
            actividadAvalada = ActividadAvalada.objects.create(**validated_data)
            return actividadAvalada

        temasData = validated_data.pop('temas')
        actividadAvalada = ActividadAvalada.objects.create(**validated_data)
        for temaData in temasData:
            Tema.objects.create(**temaData, actividadAvalada=actividadAvalada)
        return actividadAvalada
