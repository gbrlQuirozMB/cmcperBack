from rest_framework import serializers

from .models import *


class MedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'


class MedicoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'nombre', 'apPaterno', 'apMaterno', 'rfc', 'curp', 'cedProfesional', 'telJefEnse']


class MedicoAceptadoRechazadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'motivo', 'aceptado', 'numRegistro', 'nombre', 'apPaterno', 'apMaterno', 'rfc', 'telCelular']
        read_only_fields = ['aceptado', 'numRegistro','nombre','apPaterno', 'apMaterno', 'rfc', 'telCelular']
        
        
class FotoPerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'fotoPerfil']