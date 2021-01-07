from rest_framework import serializers

from .models import *


class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'


class MedicoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'nombre', 'apPaterno', 'apMaterno', 'rfc', 'curp', 'cedProfesional', 'cedEspecialidad', 'telCelular']
