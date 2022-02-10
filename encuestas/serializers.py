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


class EncuestaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Encuesta
        fields = '__all__'


# --------------------------PREGUNTAS--------------------------

class PreguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = '__all__'


class PreguntaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = '__all__'


class PreguntaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = '__all__'


# --------------------------OPCIONES--------------------------

class OpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = '__all__'


class OpcionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = '__all__'


class OpcionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = '__all__'


# --------------------------RESPUESTAS--------------------------

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = '__all__'


class RespuestaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = '__all__'


class RespuestaDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['opcionDescripcion'] = instance.opcion.descripcion
        repr['encuestaTitulo'] = instance.encuesta.titulo
        repr['preguntaDescripcion'] = instance.pregunta.descripcion
        repr['medicoNombre'] = instance.medico.nombre + ' ' + instance.medico.apPaterno + ' ' + instance.medico.apMaterno
        repr['medicoNumRegistro'] = instance.medico.numRegistro

        return repr
