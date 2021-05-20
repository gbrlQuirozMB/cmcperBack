from rest_framework import fields, serializers
from .models import *
from preregistro.models import Medico


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

    def update(self, instance, validated_data):
        instance.institucion = validated_data.get('institucion', instance.institucion)
        instance.item = validated_data.get('item', instance.item)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.emailContacto = validated_data.get('emailContacto', instance.emailContacto)
        instance.numAsistentes = validated_data.get('numAsistentes', instance.numAsistentes)
        instance.puntosAsignar = validated_data.get('puntosAsignar', instance.puntosAsignar)
        instance.fechaInicio = validated_data.get('fechaInicio', instance.fechaInicio)
        instance.lugar = validated_data.get('lugar', instance.lugar)
        instance.solicitante = validated_data.get('solicitante', instance.solicitante)
        instance.tipoPago = validated_data.get('tipoPago', instance.tipoPago)
        instance.porcentaje = validated_data.get('porcentaje', instance.porcentaje)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.isPagado = validated_data.get('isPagado', instance.isPagado)
        instance.save()

        if validated_data.get('temas') is None:
            return instance

        temasData = validated_data.pop('temas')
        Tema.objects.filter(actividadAvalada=instance.id).delete()
        for temaData in temasData:
            Tema.objects.create(**temaData, actividadAvalada=instance)
        return instance


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


class AsistenteActividadAvaladaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AsistenteActividadAvalada
        fields = '__all__'


class CuposAsistentesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadAvalada
        fields = ['numAsistentes']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        asistentesRegistrados = AsistenteActividadAvalada.objects.filter(actividadAvalada=instance.id).count()
        repr['asistentesRegistrados'] = asistentesRegistrados
        repr['porRegistrar'] = instance.numAsistentes - asistentesRegistrados

        return repr


class MedicosAIncribirseAASerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'nombre', 'apPaterno', 'apMaterno', 'rfc', 'numRegistro']


class MedicosAsistenteAASerializer(serializers.ModelSerializer):
    class Meta:
        model = AsistenteActividadAvalada
        fields = ['id']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['medicoNombre'] = instance.medico.nombre
        repr['medicoApPaterno'] = instance.medico.apPaterno
        repr['medicoEmail'] = instance.medico.email

        return repr
