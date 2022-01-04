from django.db.models import fields
from rest_framework import serializers
from .models import *
from instituciones.models import *
from preregistro.models import *


class ConceptoPagoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptoPago
        fields = '__all__'


class MonedaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneda
        fields = '__all__'


class FormaPagoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        fields = '__all__'


class UsoCFDIListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsoCFDI
        fields = '__all__'


class AvalFilteredListSerializer(serializers.ModelSerializer):  # Aval se refiere al modelo de Institucion
    class Meta:
        model = Institucion
        fields = ['nombreInstitucion', 'rfc', 'telUno', 'email', 'estado', 'deleMuni', 'colonia', 'calle', 'numInterior', 'numExterior', 'cp']


class MedicoFilteredListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'nombre', 'apPaterno', 'apMaterno', 'estadoFisc', 'deleMuniFisc', 'coloniaFisc', 'calleFisc', 'cpFisc', 'numInteriorFisc',
                  'numExteriorFisc', 'rfcFacturacion', 'usoCfdi', 'razonSocial', 'telCelular', 'email', 'numRegistro', 'isExtranjero', 'anioCertificacion']


class IdUltimaFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ['id']


class PaisListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = '__all__'


class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ['fecha', 'hora', 'tipo', 'institucion', 'medico', 'usoCFDI', 'formaPago', 'moneda', 'comentarios', 'folio', 'subtotal', 'iva', 'total', 'pais',
                  'numRegIdTrib', 'metodoPago']


class FacturaFilteredListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ['creado_en', 'folio', 'razonSocial', 'rfc', 'isCancelada', 'total', 'fecha', 'hora']


class MetodoPagoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetodoPago
        fields = '__all__'


class FacturaFilteredDownExcelSerializer(serializers.ModelSerializer):
    # tipo = serializers.CharField(source='get_tipo_display')
    class Meta:
        model = Factura
        fields = ['creado_en', 'rfc', 'razonSocial', 'estado', 'deleMuni', 'colonia', 'calle', 'numInterior', 'numExterior', 'codigoPostal', 'usoCFDI', 'formaPago',
                  'moneda', 'comentarios', 'folio', 'subtotal', 'iva', 'total', 'pais', 'numRegIdTrib', 'uuid', 'numeroCertificado', 'fechaTimbrado', 'fechaCancelado',
                  'fecha', 'hora']
        # fields = ['usoCFDI', 'formaPago', 'moneda', 'pais']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['usoCFDI'] = instance.usoCFDI.usoCFDI
        repr['formaPago'] = instance.formaPago.formaPago
        repr['moneda'] = instance.moneda.moneda
        repr['pais'] = instance.pais.pais

        return repr
