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

class AvalFilteredListSerializer(serializers.ModelSerializer):#Aval se refiere al modelo de Institucion
    class Meta:
        model = Institucion
        fields = ['nombreInstitucion', 'rfc', 'telUno', 'email', 'estado', 'deleMuni', 'colonia', 'calle', 'numInterior', 'numExterior', 'cp']

class MedicoFilteredListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'nombre', 'apPaterno', 'apMaterno', 'estadoFisc', 'deleMuniFisc', 'coloniaFisc', 'calleFisc', 'cpFisc', 'numInteriorFisc', 'numExteriorFisc', 'rfcFacturacion', 'usoCfdi', 'razonSocial', 'telCelular', 'email', 'numRegistro', 'isExtranjero', 'anioCertificacion']

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
        fields = ['fecha', 'institucion', 'medico', 'usoCFDI', 'formaPago', 'moneda', 'comentarios', 'folio', 'subtotal', 'iva', 'total', 'pais', 'numRegIdTrib']