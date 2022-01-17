from rest_framework import serializers
from .models import *


class EntregaFisicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntregaFisica
        fields = '__all__'
