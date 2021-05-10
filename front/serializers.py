from rest_framework import serializers

from .models import *


class PosicionFrontSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosicionFront
        fields = ['posicion','user']
        


# class PosicionFrontLeerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PosicionFront
#         fields = '__all__'
#         read_only_fields = [f.name for f in PosicionFront._meta.get_fields()]


class PosicionFrontLeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PosicionFront
        fields = ['posicion']
        
