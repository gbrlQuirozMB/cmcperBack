from rest_framework import fields, serializers
from .models import *
from preregistro.models import Medico
from convocatoria.models import Convocatoria, ConvocatoriaEnrolado


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
        if instance.medico != None:
            repr['medicoNombreApPaterno'] = instance.medico.nombre + ' ' + instance.medico.apPaterno

        if instance.tipo == 1:
            datoConvo = ConvocatoriaEnrolado.objects.get(id=instance.externoId)
            repr['descripcion'] = datoConvo.convocatoria.nombre
            return repr
        if instance.tipo == 2:
            repr['descripcion'] = 'Recertificación por Examen'
            return repr
        if instance.tipo == 3:
            repr['descripcion'] = 'Recertificación por Renovación'
            return repr
        # falta ver que pasa con los cursos o la actividad asistencial, si se puede traes sus datos
        repr['descripcion'] = 'No hay descripcion'

        return repr


class PagoAceptarRechazarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['id', 'estatus']
