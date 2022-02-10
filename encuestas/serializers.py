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
