from rest_framework import serializers
from .models import *
from instituciones.models import *

class ConceptoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptoPago
        fields = '__all__'

class MonedaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moneda
        fields = '__all__'

class FormaPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaPago
        fields = '__all__'

class UsoCFDISerializer(serializers.ModelSerializer):
    class Meta:
        model = UsoCFDI
        fields = '__all__'

class AvalSerializer(serializers.ModelSerializer):#Aval se refiere al modelo de Institucion
    class Meta:
        model = Institucion
        fields = ['nombreInstitucion', 'rfc', 'contacto', 'telUno', 'email']