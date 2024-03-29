from certificados.models import Certificado
from django.db.models import Sum
import datetime
from api.exceptions import *
from preregistro.models import Medico
from .models import *
from rest_framework import fields, serializers
# from api.logger import log
import logging
log = logging.getLogger('django')


class CertificadoDatosSerializer(serializers.ModelSerializer):
    estatus = serializers.CharField(source='get_estatus_display')

    class Meta:
        model = Certificado
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['nombre'] = instance.medico.nombre + ' ' + instance.medico.apPaterno
        repr['numRegistro'] = instance.medico.numRegistro
        # proximaCertificacion = instance.anioCertificacion + 5
        # repr['proximaCertificacion'] = proximaCertificacion
        # anio = int(datetime.datetime.now().strftime('%Y'))
        # repr['estatus'] = 'vigente'
        # if (proximaCertificacion - anio) == 1:
        #     repr['estatus'] = 'esta por vencer'
        # if (proximaCertificacion - anio) < 1:
        #     repr['estatus'] = 'vencido'
        return repr


class AvanceMedicoCapituloSerializer(serializers.Serializer):
    capituloDescripcion = serializers.CharField(max_length=300)
    capituloPuntos = serializers.DecimalField(max_digits=6, decimal_places=2)
    puntosOtorgados = serializers.DecimalField(max_digits=6, decimal_places=2)
    avance = serializers.DecimalField(max_digits=6, decimal_places=2)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['avance'] = str(instance.avance) + '%'
        return repr


class PuntosCapituloListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capitulo
        fields = '__all__'


class PuntosCapituloDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capitulo
        fields = '__all__'


class PorcentajeGeneralMedicoSerializer(serializers.Serializer):
    nombre = serializers.CharField(max_length=200)
    numRegistro = serializers.IntegerField()
    porcentaje = serializers.DecimalField(max_digits=6, decimal_places=2)
    puntosObtenidos = serializers.DecimalField(max_digits=6, decimal_places=2)
    puntosAReunir = serializers.DecimalField(max_digits=6, decimal_places=2)

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['porcentaje'] = str(instance.porcentaje) + '%'
        return repr


class PuntosPorCapituloMedicoSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length=150)
    descripcion = serializers.CharField(max_length=300)
    reunidos = serializers.DecimalField(max_digits=6, decimal_places=2)
    faltantes = serializers.DecimalField(max_digits=6, decimal_places=2)
    excedentes = serializers.DecimalField(max_digits=6, decimal_places=2)
    puntosCapitulo = serializers.DecimalField(max_digits=6, decimal_places=2)
    isExcedido = serializers.BooleanField()


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class SubcapituloSerializer(serializers.ModelSerializer):
    items = ItemSerializer(source='subcapituloI', read_only=True, many=True)

    class Meta:
        model = Subcapitulo
        fields = [f.name for f in model._meta.fields] + ['items']


class DetallesCapituloSerializer(serializers.ModelSerializer):
    subcapitulos = SubcapituloSerializer(source='capituloS', read_only=True, many=True)

    class Meta:
        model = Capitulo
        fields = [f.name for f in model._meta.fields] + ['subcapitulos']


class ItemDocumentosSerializer(serializers.ModelSerializer):
    estatus = serializers.CharField(source='get_estatus_display')

    class Meta:
        model = RecertificacionItemDocumento
        fields = '__all__'


class ItemDocumentoSerializer(serializers.ModelSerializer):
    estatusDescripcion = serializers.CharField(source='get_estatus_display', read_only=True)

    class Meta:
        model = RecertificacionItemDocumento
        fields = [f.name for f in model._meta.fields] + ['estatusDescripcion']


class CertificadosMedicoListSerialializer(serializers.ModelSerializer):
    estatus = serializers.CharField(source='get_estatus_display')

    class Meta:
        model = Certificado
        fields = '__all__'


class ItemDocumentoFilteredSerializer(serializers.ModelSerializer):
    estatus = serializers.CharField(source='get_estatus_display', read_only=True)

    class Meta:
        model = RecertificacionItemDocumento
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['capitulo'] = instance.item.subcapitulo.capitulo.descripcion
        repr['medico'] = instance.medico.nombre + ' ' + instance.medico.apPaterno
        repr['medicoId'] = instance.medico.id
        try:
            certificadoMedico = Certificado.objects.filter(medico=instance.medico, isVencido=False)[0]
            repr['fechaCertificacion'] = certificadoMedico.fechaCertificacion
        except:
            repr['fechaCertificacion'] = 'no existe certificado'

        return repr


class ItemDocumentoDetailSerializer(serializers.ModelSerializer):
    estatusDescripcion = serializers.CharField(source='get_estatus_display', read_only=True)

    class Meta:
        model = RecertificacionItemDocumento
        fields = [f.name for f in model._meta.fields] + ['estatusDescripcion']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['capitulo'] = instance.item.subcapitulo.capitulo.descripcion
        repr['subcapitulo'] = instance.item.subcapitulo.descripcion
        repr['nombreCompleto'] = instance.medico.nombre + ' ' + instance.medico.apPaterno + ' ' + instance.medico.apPaterno
        repr['puntosItem'] = instance.item.puntos
        repr['item'] = instance.item.descripcion
        # try:
        #     certificadoMedico = Certificado.objects.filter(medico=instance.medico, isVencido=False)[0]
        #     repr['fechaCertificacion'] = certificadoMedico.fechaCertificacion
        # except:
        #     repr['fechaCertificacion'] = 'no existe certificado'

        return repr


class ItemDocumentoAceptarRechazarSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecertificacionItemDocumento
        fields = ['id', 'puntosOtorgados', 'estatus', 'notasRechazo', 'razonRechazo', 'observaciones']


class ItemDocumentoReasignarSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecertificacionItemDocumento
        fields = ['id', 'puntosOtorgados', 'estatus', 'notasRechazo', 'razonRechazo', 'observaciones', 'item']


class CapituloListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capitulo
        fields = ['id', 'titulo', 'descripcion']


class CapituloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Capitulo
        fields = '__all__'


class SubcapituloUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcapitulo
        fields = '__all__'


class SubcapituloListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcapitulo
        fields = '__all__'


class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class SolicitudExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PorExamen
        fields = '__all__'


class PorExamenDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PorExamenDocumento
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['tipoDocumento'] = instance.catTiposDocumento.descripcion
        return repr


class MedicoAPagarExamenSerializer(serializers.ModelSerializer):

    class Meta:
        model = CatPagos
        fields = ['descripcion', 'precio']  # OJO: no envio el id porque puede confundir

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        medicoId = self.context.get('medicoId')  # recibimos variable extra!!!
        datoMedico = Medico.objects.get(id=medicoId)
        repr['medico'] = datoMedico.nombre + ' ' + datoMedico.apPaterno
        datoPorExamen = PorExamen.objects.get(medico=medicoId, isAceptado=True)
        repr['porExamenId'] = datoPorExamen.id
        repr['tipo'] = 1

        return repr


class MedicoAPagarRenovacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatPagos
        fields = ['descripcion', 'precio']  # OJO: no envio el id porque puede confundir

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        medicoId = self.context.get('medicoId')  # recibimos variable extra!!!
        datoMedico = Medico.objects.get(id=medicoId)
        repr['medico'] = datoMedico.nombre + ' ' + datoMedico.apPaterno
        repr['tipo'] = 6

        return repr


class PorExamenPagadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PorExamen
        fields = ['id', 'isPagado']


class CertificadoPagadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = ['medico', 'estatus', 'descripcion', 'isVencido']


class PorExamenFilteredListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PorExamen
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['nombreCompleto'] = instance.medico.nombre + ' ' + instance.medico.apPaterno

        return repr


class PorExamenDocumentoAceptarRechazarSerializer(serializers.ModelSerializer):
    class Meta:
        model = PorExamenDocumento
        fields = ['id', 'isAceptado']


class PorExamenMedicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PorExamen
        fields = '__all__'


class FechasExamenRecertificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FechasExamenRecertificacion
        fields = '__all__'


class ProrrogaCertificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificado
        fields = ['id', 'fechaCertificacion']


class RenovacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renovacion
        fields = '__all__'


class DetallesSubcapituloSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcapitulo
        fields = '__all__'


class QRItemDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecertificacionItemDocumento
        fields = ['id', 'documento']


class PorExamenFechaCalificarSerializer(serializers.ModelSerializer):
    class Meta:
        model = PorExamen
        fields = ['id', 'calificacion', 'isAprobado']
