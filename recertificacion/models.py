from django.db import models
from django.core.validators import FileExtensionValidator
from preregistro.models import Medico
from catalogos.models import *
import datetime


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


class RecertificacionDocumento(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medicoR')
    catTiposDocumento = models.ForeignKey(CatTiposDocumento, on_delete=models.CASCADE, related_name='catTiposDocumentoR')
    documento = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif'])])
    isValidado = models.BooleanField(default=False, db_column='is_validado')
    notasValidado = models.TextField(blank=True, db_column='notas_validado')
    rechazoValidado = models.CharField(max_length=200, blank=True, db_column='rechazo_validado')

    class Meta:
        db_table = 'recertificacion_documentos'
        ordering = ['-actualizado_en']


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