from django.db.models import fields
from rest_framework import serializers
from .models import *
from instituciones.models import *
from preregistro.models import *
from api.exceptions import *


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
        fields = ['fecha', 'tipo', 'institucion', 'medico', 'usoCFDI', 'formaPago', 'moneda', 'comentarios', 'folio', 'subtotal', 'iva', 'total', 'pais',
                  'numRegIdTrib', 'metodoPago', 'codigoPostal']

    def validate(self, data):
        if 'usoCFDI' not in data or data.get('usoCFDI') is None:
            # raise serializers.ValidationError('chingao')
            raise CampoIncorrecto({"usoCFDI": ["Este campo es requerido y/o debe contener un valor válido "]})

        if 'formaPago' not in data or data.get('formaPago') is None:
            raise CampoIncorrecto({"formaPago": ["Este campo es requerido y/o debe contener un valor válido "]})

        if 'moneda' not in data or data.get('moneda') is None:
            raise CampoIncorrecto({"moneda": ["Este campo es requerido y/o debe contener un valor válido "]})

        if 'pais' not in data or data.get('pais') is None:
            raise CampoIncorrecto({"pais": ["Este campo es requerido y/o debe contener un valor válido "]})

        if 'metodoPago' not in data or data.get('metodoPago') is None:
            raise CampoIncorrecto({"metodoPago": ["Este campo es requerido y/o debe contener un valor válido "]})

        return data

    def create(self, validated_data):
        factura = Factura.objects.filter()[:1]
        if factura.count() != 0:
            valor = int(factura.get().folio)
            valor += 1
            validated_data.update({'folio': valor})
        else:
            validated_data.update({'folio': 1})

        return Factura(**validated_data)
    
    # def to_representation(self, value):
    #     # fecha = time.strftime('%M:%S', time.gmtime(value.duration))
    #     fecha = serializers.DateTimeField('%Y-%m-%dT%H:%M:%SZ').to_representation(value.fecha)
    #     # fecha = (value.fecha)
    #     # return 'Track %d: %s (%s)' % (value.order, value.name, duration)
    #     return fecha
    
    
    # def get_fecha(self, instance) -> str:

    #     representation: str = serializers.DateTimeField('%Y-%m-%dT%H:%M:%SZ').to_representation(instance.fecha)
    #     return representation
    


class FacturaFilteredListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'
        # fields = ['creado_en', 'folio', 'razonSocial', 'rfc', 'isCancelada', 'total', 'fecha', 'hora']


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
                  'fecha']
        # fields = ['usoCFDI', 'formaPago', 'moneda', 'pais']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['usoCFDI'] = instance.usoCFDI.usoCFDI
        repr['formaPago'] = instance.formaPago.formaPago
        repr['moneda'] = instance.moneda.moneda
        repr['pais'] = instance.pais.pais

        return repr
