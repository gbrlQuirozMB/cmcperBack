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
        
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        try:
            datoMedico = Medico.objects.get(numRegistro=instance.destinatario)
            repr['fotoPerfil'] = datoMedico.fotoPerfil.url
        except:
            repr['fotoPerfil'] = None

        return repr


class MedicoChatListSerializer(serializers.ModelSerializer):
    nombreCompleto = serializers.SerializerMethodField()

    class Meta:
        model = Medico
        fields = ['id', 'nombreCompleto', 'numRegistro', 'fotoPerfil']

    def get_nombreCompleto(self, obj):
        return obj.nombre + ' ' + obj.apPaterno + ' ' + obj.apMaterno
