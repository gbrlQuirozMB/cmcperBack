from preregistro.models import Medico
from .models import *
from rest_framework import fields, serializers
from api.logger import log
from api.exceptions import *

import datetime
from django.db.models import Sum


class CertificadoDatosSerializer(serializers.ModelSerializer):
    estatus = serializers.CharField(source='get_estatus_display')

    class Meta:
        model = Certificado
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['nombre'] = instance.medico.nombre + ' ' + instance.medico.apPaterno
        repr['numRegistro'] = instance.medico.numRegistro
        # proximaCertificacion = instance.anioCertificacion + 5
        # repr['proximaCertificacion'] = proximaCertificacion
        # anio = int(datetime.datetime.now().strftime('%Y'))
        # repr['estatus'] = 'vigente'
        # if (proximaCertificacion - anio) == 1:
        #     repr['estatus'] = 'esta por vencer'
        # if (proximaCertificacion - anio) < 1:
        #     repr['estatus'] = 'vencido'
        return repr


class AvanceMedicoCapituloSerializer(serializers.Serializer):
    capituloDescripcion = serializers.CharField(max_length=300)
    capituloPuntos = serializers.DecimalField(max_digits=6, decimal_places=2)
    puntosOtorgados = serializers.DecimalField(max_digits=6, decimal_places=2)
    avance = serializers.DecimalField(max_digits=6, decimal_places=2)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['avance'] = str(instance.avance) + '%'
        return repr


class PuntosCapituloListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capitulo
        fields = '__all__'


class PuntosCapituloDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capitulo
        fields = '__all__'


class PorcentajeGeneralMedicoSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=200)
    numRegistro = serializers.IntegerField()
    porcentaje = serializers.DecimalField(max_digits=6, decimal_places=2)
    puntosObtenidos = serializers.DecimalField(max_digits=6, decimal_places=2)
    puntosAReunir = serializers.DecimalField(max_digits=6, decimal_places=2)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['porcentaje'] = str(instance.porcentaje) + '%'
        return repr


class PuntosPorCapituloMedicoSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length=150)
    descripcion = serializers.CharField(max_length=300)
    reunidos = serializers.DecimalField(max_digits=6, decimal_places=2)
    faltantes = serializers.DecimalField(max_digits=6, decimal_places=2)
    excedentes = serializers.DecimalField(max_digits=6, decimal_places=2)
    puntosCapitulo = serializers.DecimalField(max_digits=6, decimal_places=2)
    isExcedido = serializers.BooleanField()


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class SubcapituloSerializer(serializers.ModelSerializer):
    items = ItemSerializer(source='subcapituloI', read_only=True, many=True)

    class Meta:
        model = Subcapitulo
        fields = [f.name for f in model._meta.fields] + ['items']


class DetallesCapituloSerializer(serializers.ModelSerializer):
    subcapitulos = SubcapituloSerializer(source='capituloS', read_only=True, many=True)

    class Meta:
        model = Capitulo
        fields = [f.name for f in model._meta.fields] + ['subcapitulos']
