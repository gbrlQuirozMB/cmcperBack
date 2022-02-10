from rest_framework import serializers
from .models import *


class EncuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encuesta
        fields = '__all__'


class EncuestaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encuesta
        fields = '__all__'
