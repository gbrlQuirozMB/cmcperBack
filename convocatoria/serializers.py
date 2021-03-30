from preregistro.models import Medico
from .models import *
from rest_framework import fields, serializers
from api.logger import log
from api.exceptions import *


class EsExtranjeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'isExtranjero', 'nacionalidad']


class EstudioExtranjeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = ['id', 'estudioExtranjero', 'escuelaExtranjero']


class SedeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sede
        fields = ['catSedes']


class TipoExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoExamen
        fields = ['catTiposExamen']


class ConvocatoriaSerializer(serializers.ModelSerializer):
    sedes = SedeSerializer(required=True, many=True)
    tiposExamen = TipoExamenSerializer(required=False, many=True)

    class Meta:
        model = Convocatoria
        # evito poner todo el listado de campos
        # fields = [f.name for f in model._meta.fields] + ['sedes'] + ['tiposExamen']
        # read_only_fields = ['archivo','banner']
        fields = ['id', 'fechaInicio', 'fechaTermino', 'fechaExamen', 'horaExamen', 'nombre', 'detalles', 'sedes', 'tiposExamen', 'fechaResolucion']
        # depth = 2

    def create(self, validated_data):
        sedesData = validated_data.pop('sedes')
        for dato in sedesData:
            if not bool(dato):
                log.info(f'campos incorrectos: catSedes')
                raise CamposIncorrectos({"catSedes": ["Este campo es requerido"]})

        tiposExameneData = validated_data.pop('tiposExamen')
        for dato in tiposExameneData:
            if not bool(dato):
                log.info(f'campos incorrectos: catTiposExamen')
                raise CamposIncorrectos({"catTiposExamen": ["Este campo es requerido"]})

        convocatoria = Convocatoria.objects.create(**validated_data)
        for sedeData in sedesData:
            Sede.objects.create(**sedeData, convocatoria=convocatoria)
        for tipoExamenData in tiposExameneData:
            TipoExamen.objects.create(**tipoExamenData, convocatoria=convocatoria)
        # return validated_data # incompleto porque ya se le quito la llave 'sedes' y 'tiposExamen'
        return convocatoria

    def update(self, instance, validated_data):
        sedesData = validated_data.pop('sedes')
        for dato in sedesData:

            if not bool(dato):
                log.info(f'campos incorrectos: catSedes')
                raise CamposIncorrectos({"catSedes": ["Este campo es requerido"]})

        tiposExameneData = validated_data.pop('tiposExamen')
        for dato in tiposExameneData:
            if not bool(dato):
                log.info(f'campos incorrectos: catTiposExamen')
                raise CamposIncorrectos({"catTiposExamen": ["Este campo es requerido"]})

        instance.fechaInicio = validated_data.get('fechaInicio', instance.fechaInicio)
        instance.fechaTermino = validated_data.get('fechaTermino', instance.fechaTermino)
        instance.fechaExamen = validated_data.get('fechaExamen', instance.fechaExamen)
        instance.horaExamen = validated_data.get('horaExamen', instance.horaExamen)
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.detalles = validated_data.get('detalles', instance.detalles)
        instance.save()

        Sede.objects.filter(convocatoria=instance.id).delete()
        for sedeData in sedesData:
            Sede.objects.create(**sedeData, convocatoria=instance)

        TipoExamen.objects.filter(convocatoria=instance.id).delete()
        for tipoExamenData in tiposExameneData:
            TipoExamen.objects.create(**tipoExamenData, convocatoria=instance)

        return instance


class ConvocatoriaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convocatoria
        # fields = ['id', 'nombre']
        fields = ['id', 'nombre', 'fechaInicio', 'fechaTermino', 'fechaExamen']


class CatSedesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatSedes
        fields = '__all__'


class SedeGetDetailSerializer(serializers.ModelSerializer):
    catSedes = CatSedesSerializer(read_only=True)

    class Meta:
        model = Sede
        fields = ['catSedes']


class CatTiposExamenSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatTiposExamen
        fields = '__all__'


class TiposExamenGetDetailSerializer(serializers.ModelSerializer):
    catTiposExamen = CatTiposExamenSerializer(read_only=True)

    class Meta:
        model = TipoExamen
        fields = ['catTiposExamen']


class ConvocatoriaGetDetailSerializer(serializers.ModelSerializer):
    sedes = SedeGetDetailSerializer(read_only=True, many=True)
    tiposExamen = TiposExamenGetDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Convocatoria
        fields = [f.name for f in model._meta.fields] + ['sedes'] + ['tiposExamen']


class ConvocatoriaArchivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convocatoria
        fields = ['id', 'archivo']


class ConvocatoriaBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Convocatoria
        fields = ['id', 'banner']


class ConvocatoriaEnroladoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnrolado
        fields = '__all__'


class ConvocatoriaEnroladoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnroladoDocumento
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        # dato = CatTiposDocumento.objects.get(id=instance.catTiposDocumento.id)
        # repr['tipoDocumento'] = dato.descripcion
        repr['tipoDocumento'] = instance.catTiposDocumento.descripcion
        return repr


class ConvocatoriaEnroladoDocumentoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnroladoDocumento
        fields = ['id', 'documento', 'isValidado', 'rechazoValidado', 'notasValidado', 'engargoladoOk', 'rechazoEngargolado', 'notasEngargolado']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        # dato = CatTiposDocumento.objects.get(id=instance.catTiposDocumento.id)
        # repr['tipoDocumento'] = dato.descripcion
        repr['tipoDocumento'] = instance.catTiposDocumento.descripcion
        return repr


class ConvocatoriaDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnroladoDocumento
        fields = ['id', 'documento']


class ConvocatoriaEnroladoMedicoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnrolado
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['catTiposExamen'] = instance.catTiposExamen.descripcion
        repr['catSedes'] = instance.catSedes.descripcion
        repr['convocatoriaId'] = instance.convocatoria.id
        repr['convocatoria'] = instance.convocatoria.nombre
        repr['medico'] = instance.medico.nombre + ' ' + instance.medico.apPaterno
        return repr


class ConvocatoriaEnroladosMedicoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnrolado
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['catTiposExamen'] = instance.catTiposExamen.descripcion
        repr['catSedes'] = instance.catSedes.descripcion
        repr['convocatoria'] = instance.convocatoria.nombre
        repr['convocatoriaId'] = instance.convocatoria.id
        repr['medico'] = instance.medico.nombre + ' ' + instance.medico.apPaterno
        repr['medicoId'] = instance.medico.id
        return repr


class ConvocatoriaEnroladoComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnrolado
        fields = ['id', 'comentario']


class ConvocatoriaEnroladoDocumentoAceptarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnroladoDocumento
        fields = ['id', 'isValidado', 'notasValidado', 'rechazoValidado']


class ConvocatoriaEnroladoDocumentoRechazarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnroladoDocumento
        fields = ['id', 'isValidado', 'notasValidado', 'rechazoValidado']


class ConvocatoriaEnroladoEngargoladoAceptarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnroladoDocumento
        fields = ['id', 'engargoladoOk', 'notasEngargolado', 'rechazoEngargolado']


class ConvocatoriaEnroladoEngargoladoRechazarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnroladoDocumento
        fields = ['id', 'engargoladoOk', 'notasEngargolado', 'rechazoEngargolado']


class ConvocatoriaEnroladoMedicoAPagarDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnrolado
        fields = ['id', 'medico', 'convocatoria', 'catSedes', 'catTiposExamen']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['catTiposExamen'] = instance.catTiposExamen.descripcion
        repr['catSedes'] = instance.catSedes.descripcion
        repr['convocatoria'] = instance.convocatoria.nombre
        repr['medico'] = instance.medico.nombre + ' ' + instance.medico.apPaterno
        repr['aPagar'] = instance.catTiposExamen.precio
        if instance.medico.estudioExtranjero:
            repr['aPagar'] = instance.catTiposExamen.precioExtrangero
        return repr


class ConvocatoriaEnroladoMedicoPagadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnrolado
        fields = ['id', 'isPagado']


class ConvocatoriaPagoSerializer(serializers.ModelSerializer):
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
        repr['convocatoriaEnrolado'] = instance.convocatoriaEnrolado.convocatoria.nombre
        repr['medicoNombreApPaterno'] = instance.medico.nombre + ' ' + instance.medico.apPaterno
        return repr


class PagoAceptarRechazarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['id', 'estatus']
