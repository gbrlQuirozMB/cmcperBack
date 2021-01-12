from preregistro.models import Medico
from rest_framework import serializers

from .models import *


class MensajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mensaje
        fields = '__all__'
        
        
class ConversacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversacion
        fields = '__all__'
        
        
class MedicoChatListSerializer(serializers.ModelSerializer):
    nombreCompleto = serializers.SerializerMethodField()
    class Meta:
        model = Medico
        fields = ['id','nombreCompleto','numRegistro']
    
    def get_nombreCompleto(self, obj):
        return obj.nombre + ' ' + obj.apPaterno + ' ' + obj.apMaterno