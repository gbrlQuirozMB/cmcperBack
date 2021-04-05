from django.db import models
from django.core.validators import FileExtensionValidator
from preregistro.models import Medico
from catalogos.models import *


# Create your models here.
class Capitulo(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=300)
    puntos = models.DecimalField(max_digits=6, decimal_places=2)
    maximo = models.DecimalField(max_digits=6, decimal_places=2)
    minimo = models.DecimalField(max_digits=6, decimal_places=2)
    isOpcional = models.BooleanField(default=False, db_column='is_opcional')
    icono = models.FileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif'])])

    class Meta:
        db_table = 'capitulos'
        ordering = ['-titulo']


class Subcapitulo(models.Model):
    descripcion = models.CharField(max_length=300)
    comentarios = models.TextField(blank=True, null=True)
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE, related_name='subcapituloC')

    class Meta:
        db_table = 'subcapitulos'
        ordering = ['capitulo']


class Item(models.Model):
    descripcion = models.CharField(max_length=300)
    puntos = models.DecimalField(max_digits=6, decimal_places=2)
    subcapitulo = models.ForeignKey(Subcapitulo, on_delete=models.CASCADE, related_name='itemS')

    class Meta:
        db_table = 'items'
        ordering = ['subcapitulo']


class Certificado(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medicoC')
    catTiposDocumento = models.ForeignKey(CatTiposDocumento, on_delete=models.CASCADE, related_name='catTiposDocumentoC')
    documento = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif'])])
    descripcion = models.CharField(max_length=300)
    isVencido = models.BooleanField(default=False, db_column='is_vencido')
    anioInicio = models.SmallIntegerField(db_column='anio_inicio')

    class Meta:
        db_table = 'certificados'
        ordering = ['-actualizado_en']


class PorExamen(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medicoPE')
    estatus = models.PositiveSmallIntegerField(blank=True, choices=(
        (1, 'Aceptado'),
        (2, 'Rechazado'),
        (3, 'Pendiente')
    ))
    isAprobado = models.BooleanField(default=False, db_column='is_aprobado')  # verificar si se le da su certificado
    calificacion = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'recertificacion_por_examen'
        ordering = ['-actualizado_en']


class PorExamenDocumento(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medicoD')
    catTiposDocumento = models.ForeignKey(CatTiposDocumento, on_delete=models.CASCADE, related_name='catTiposDocumentoD')
    porExamen = models.ForeignKey(PorExamen, on_delete=models.CASCADE, related_name='porExamenD')
    documento = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif'])])
    isAceptado = models.BooleanField(default=False, db_column='is_aceptado')

    class Meta:
        db_table = 'recertificacion_por_examen_documentos'
        ordering = ['-actualizado_en']
