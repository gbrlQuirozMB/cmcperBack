from rest_framework import serializers
from .models import *


class ComunicadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comunicado
        fields = '__all__'
