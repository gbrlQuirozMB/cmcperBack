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


class ActividadAvaladaArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadAvalada
        fields = ['id', 'archivo']


class ActividadAvaladaBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadAvalada
        fields = ['id', 'banner']


class ActividadAvaladaFilteredListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadAvalada
        fields = ['id', 'institucion', 'item', 'fechaInicio', 'isPagado', 'puntosAsignar']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['institucion'] = instance.institucion.nombreInstitucion
        repr['capitulo'] = instance.item.subcapitulo.capitulo.descripcion
        repr['subcapitulo'] = instance.item.subcapitulo.descripcion

        return repr


class ActividadAvaladaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadAvalada
        fields = '__all__'
