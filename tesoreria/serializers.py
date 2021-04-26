from rest_framework import fields, serializers
from .models import *
from preregistro.models import Medico
from convocatoria.models import Convocatoria


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'


class PagosListSerializer(serializers.ModelSerializer):
    estatus = serializers.CharField(source='get_estatus_display')

    class Meta:
        model = Pago
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        if instance.tipo == 1:
            # repr['convocatoriaEnrolado'] = instance.convocatoriaEnrolado.convocatoria.nombre
            datoConvo = Convocatoria.objects.id(instance.externoId)
            repr['convocatoria'] = datoConvo.nombre
        if instance.medico != None:
            repr['medicoNombreApPaterno'] = instance.medico.nombre + ' ' + instance.medico.apPaterno
        return repr


class PagoAceptarRechazarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['id', 'estatus']
