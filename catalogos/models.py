from django.db import models
from django.core.validators import FileExtensionValidator


# Create your models here.
class CatSedes(models.Model):
    descripcion = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    imagen = models.FileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'gif', 'jpeg'])], upload_to='catalogos')

    class Meta:
        db_table = 'cat_sedes'
        ordering = ['descripcion']


class CatTiposExamen(models.Model):
    descripcion = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    precioExtrangero = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    class Meta:
        db_table = 'cat_tipos_examen'
        ordering = ['descripcion']


class CatTiposDocumento(models.Model):
    descripcion = models.CharField(max_length=200)

    class Meta:
        db_table = 'cat_tipos_documento'
        ordering = ['descripcion']


class CatMotivosRechazo(models.Model):
    descripcion = models.CharField(max_length=300)
    tipo = models.PositiveSmallIntegerField(blank=True, choices=(
        (1, 'Validación'),
        (2, 'Engargolado')
    ))

    class Meta:
        db_table = 'cat_motivos_rechazo'
        ordering = ['descripcion']


class CatPagos(models.Model):
    descripcion = models.CharField(max_length=200)
    precio = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    # tipo = models.PositiveSmallIntegerField(choices=(
    #     (1, 'Examen Certificación Vigente'),
    #     (2, 'Examen Convocatoria Nacional'),
    #     (3, 'Examen Convocatoria Extranjero'),
    #     (4, 'Curso'),
    #     (5, 'Actividad Asistencial'),
    #     (6, 'Renovación de Certificación'),
    # ))

    class Meta:
        db_table = 'cat_pagos'
        ordering = ['descripcion']

class CatEntidad(models.Model):
    entidad = models.CharField(max_length = 50)
    region = models.CharField(max_length = 50)
    class Meta:
        db_table = 'cat_entidad'