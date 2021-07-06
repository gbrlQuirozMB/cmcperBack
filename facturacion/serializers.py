from rest_framework import serializers
from .models import *

class ConceptoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConceptoPago
        fields = '__all__'