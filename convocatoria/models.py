from django.db import models
from django.core.validators import FileExtensionValidator
from catalogos.models import *
from preregistro.models import Medico
# Create your models here.


class Convocatoria(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    fechaInicio = models.DateField(db_column='fecha_inicio')
    fechaTermino = models.DateField(db_column='fecha_termino')
    fechaExamen = models.DateField(db_column='fecha_examen')
    horaExamen = models.TimeField(db_column='hora_examen')
    nombre = models.CharField(max_length=150)
    archivo = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])], upload_to='convocatoria')
    banner = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'gif', 'jpeg'])], upload_to='convocatoria')
    detalles = models.TextField(blank=True)
    fechaResolucion = models.DateField(blank=True, null=True, db_column='fecha_resolucion')

    class Meta:
        db_table = 'convocatoria'
        ordering = ['-creado_en']


class Sede(models.Model):
    catSedes = models.ForeignKey(CatSedes, on_delete=models.SET_NULL, null=True, related_name='catSedes')
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE, related_name='sedes')

    class Meta:
        db_table = 'sede'
        ordering = ['-catSedes']


class TipoExamen(models.Model):
    catTiposExamen = models.ForeignKey(CatTiposExamen, on_delete=models.SET_NULL, null=True, related_name='catTiposExamen')
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE, related_name='tiposExamen')

    class Meta:
        db_table = 'tipo_examen'
        ordering = ['-catTiposExamen']


class ConvocatoriaEnrolado(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medicoE')
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE, related_name='convocatoriaE')
    catSedes = models.ForeignKey(CatSedes, on_delete=models.CASCADE, null=True, related_name='catSedesE')
    catTiposExamen = models.ForeignKey(CatTiposExamen, on_delete=models.CASCADE, null=True, related_name='catTiposExamenE')
    comentario = models.TextField(blank=True)
    isPagado = models.BooleanField(default=False, db_column='is_pagado') # verificar si ya pago
    isAceptado = models.BooleanField(default=False, db_column='is_aceptado') # se activa para validar que aceptaron todos sus documentos y engargolados
    calificacion = models.DecimalField(blank=True, null=True, max_digits=6, decimal_places=2) # ahora se pide que sea decimal
    # certificado = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif'])])
    isAprobado = models.BooleanField(default=False, db_column='is_aprobado') # verificar si se le da su certificado
    isPublicado = models.BooleanField(default=False, db_column='is_publicado') # verificar si se le da su certificado por primera vez
    

    class Meta:
        db_table = 'convocatorias_enrolados'
        ordering = ['-actualizado_en']


class ConvocatoriaEnroladoDocumento(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medicoD')
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE, related_name='convocatoriaD')
    catTiposDocumento = models.ForeignKey(CatTiposDocumento, on_delete=models.CASCADE, related_name='catTiposDocumentoD')
    documento = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif', 'jpeg'])], upload_to='convocatoria')
    isValidado = models.BooleanField(default=False, db_column='is_validado')
    engargoladoOk = models.BooleanField(default=False, db_column='engargolado_ok')
    notasValidado = models.TextField(blank=True, db_column='notas_validado')
    notasEngargolado = models.TextField(blank=True, db_column='notas_engargolado')
    rechazoValidado = models.CharField(max_length=200, blank=True, db_column='rechazo_validado')
    rechazoEngargolado = models.CharField(max_length=200, blank=True, db_column='rechazo_engargolado')

    class Meta:
        db_table = 'convocatorias_enrolados_documentos'
        ordering = ['-actualizado_en']
