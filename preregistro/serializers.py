from django.db.models import fields
from rest_framework import serializers

from .models import *


class MedicoSerializer(serializers.ModelSerializer):
    fotoPerfil = serializers.SerializerMethodField()
    class Meta:
        model = Medico
        fields = '__all__'
    
    def get_fotoPerfil(self, obj):
        return obj.fotoPerfil.url if obj.fotoPerfil else None


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
        

class HorarioAtencionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioAtencion
        fields = '__all__'
        
class NotasObservacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotasObservaciones
        fields = '__all__'