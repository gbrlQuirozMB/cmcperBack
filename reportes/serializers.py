from rest_framework import fields, serializers
from .models import *
from preregistro.models import Medico
from convocatoria.models import *
from certificados.models import Certificado


class MedResidenteListSerializer(serializers.ModelSerializer):
    sexo = serializers.CharField(source='get_sexo_display', read_only=True)

    class Meta:
        model = Medico
        fields = ['id', 'telConsultorio', 'telParticular', 'telJefEnse', 'email', 'sexo', 'ciudad', 'estudioExtranjero', 'isExtranjero']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['nombreCompleto'] = instance.nombre + ' ' + instance.apPaterno + ' ' + instance.apMaterno

        return repr


class MedResidenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'


class MedResidenteExtrasDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnrolado
        fields = ['catSedes', 'catTiposExamen']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['catTiposExamen'] = instance.catTiposExamen.descripcion
        repr['catSedes'] = instance.catSedes.descripcion

        return repr


class MedCertificadoListSerializer(serializers.ModelSerializer):
    sexo = serializers.CharField(source='get_sexo_display', read_only=True)

    class Meta:
        model = Medico
        fields = ['id', 'numRegistro', 'telConsultorio', 'telParticular', 'telCelular', 'email', 'sexo']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['nombreCompleto'] = instance.nombre + ' ' + instance.apPaterno + ' ' + instance.apMaterno
        try:
            dato = Certificado.objects.filter(medico=instance.id)[0]
            repr['estatusVigencia'] = dato.get_estatus_display()
        except:
            repr['estatusVigencia'] = 'No existe'

        return repr


class MedCertificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medico
        fields = '__all__'


class MedCertificadoFechasSerializer(serializers.ModelSerializer):
    estatus = serializers.CharField(source='get_estatus_display')

    class Meta:
        model = Certificado
        fields = ['fechaCertificacion', 'fechaCaducidad', 'estatus']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['nombre'] = instance.medico.nombre + ' ' + instance.medico.apPaterno
        repr['numRegistro'] = instance.medico.numRegistro
        anio = int(instance.fechaCaducidad.strftime('%Y'))
        repr['anioProxima'] = anio

        return repr


class MedResidenteDocumentosFilteredListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConvocatoriaEnrolado
        fields = ['medico']

    def to_representation(self, instance):
        repr = super().to_representation(instance)

        repr['estudioExtranjero'] = instance.medico.estudioExtranjero
        repr['nombreCompleto'] = instance.medico.nombre + ' ' + instance.medico.apPaterno + ' ' + instance.medico.apMaterno
        cuentaTotal = ConvocatoriaEnroladoDocumento.objects.filter(medico=instance.medico, convocatoria=instance.convocatoria).count()
        repr['cuentaTotal'] = cuentaTotal
        cuentaDigitales = ConvocatoriaEnroladoDocumento.objects.filter(medico=instance.medico, convocatoria=instance.convocatoria, isValidado=True).count()
        repr['cuentaDigitales'] = cuentaDigitales  # * 100 / cuentaTotal
        cuentaEngargolados = ConvocatoriaEnroladoDocumento.objects.filter(medico=instance.medico, convocatoria=instance.convocatoria, engargoladoOk=True).count()
        repr['cuentaEngargolados'] = cuentaEngargolados  # * 100 / cuentaTotal

        return repr


class DirectorioListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medico
        fields = ['numRegistro', 'nombre', 'apPaterno', 'apMaterno', 'titulo', 'telConsultorioPublico', 'telCelularPublico', 'email', 'facebook', 'instagram', 'twitter', 'pagWeb', 'whatsapp',
                  'paisConsult', 'estadoConsult', 'ciudadConsult', 'deleMuniConsult', 'coloniaConsult', 'calleConsult', 'cpConsult', 'numInteriorConsult', 'numExteriorConsult',
                  'univEgreso', 'isCertificado']

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        # repr['nombreCompleto'] = instance.nombre + ' ' + instance.apPaterno + ' ' + instance.apMaterno
        try:
            dato = Certificado.objects.filter(medico=instance.id)[0]
            repr['ultimaCertificacion'] = dato.fechaCertificacion
            repr['ultimoCertificado'] = dato.id
            
        except:
            repr['ultimaCertificacion'] = 'No existe'
            repr['ultimoCertificado'] = 'No existe'

        return repr
