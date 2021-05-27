from django.db import models
from django.core.validators import FileExtensionValidator
from preregistro.models import Medico
from catalogos.models import *

import datetime
from dateutil.relativedelta import relativedelta
# Create your models here.


class Capitulo(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=300)
    puntos = models.DecimalField(max_digits=6, decimal_places=2)
    maximo = models.DecimalField(max_digits=6, decimal_places=2)
    minimo = models.DecimalField(max_digits=6, decimal_places=2)
    isOpcional = models.BooleanField(default=False, db_column='is_opcional')
    icono = models.FileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif'])], upload_to='recertificacion')

    class Meta:
        db_table = 'capitulos'
        ordering = ['-titulo']


class Subcapitulo(models.Model):
    descripcion = models.CharField(max_length=300)
    comentarios = models.TextField(blank=True, null=True)
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE, related_name='capituloS')

    class Meta:
        db_table = 'subcapitulos'
        ordering = ['capitulo']


class Item(models.Model):
    descripcion = models.CharField(max_length=300)
    puntos = models.DecimalField(max_digits=6, decimal_places=2)
    subcapitulo = models.ForeignKey(Subcapitulo, on_delete=models.CASCADE, related_name='subcapituloI')

    class Meta:
        db_table = 'items'
        ordering = ['subcapitulo']


class FechasExamenRecertificacion(models.Model):
    actualizado_en = models.DateTimeField(auto_now=True)
    fechaExamen = models.DateField(db_column='fecha_examen')
    descripcion = models.CharField(max_length=300)

    class Meta:
        db_table = 'fechas_examen_recertificacion'
        ordering = ['-fechaExamen']


class PorExamen(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medicoPE')
    fechaExamen = models.ForeignKey(FechasExamenRecertificacion, on_delete=models.CASCADE, null=True, related_name='fechaExamenPE')
    estatus = models.PositiveSmallIntegerField(blank=True, choices=(
        (1, 'Aceptado'),
        (2, 'Rechazado'),
        (3, 'Pendiente')
    ))
    isAprobado = models.BooleanField(default=False, db_column='is_aprobado')  # verificar si se le da su certificado
    calificacion = models.PositiveSmallIntegerField(blank=True, null=True)
    isPagado = models.BooleanField(default=False, db_column='is_pagado')  # verificar si ya pago
    isAceptado = models.BooleanField(default=False, db_column='is_aceptado')  # se activa para validar que aceptaron todos sus documentos
    isPublicado = models.BooleanField(default=False, db_column='is_publicado')  # verificar si se le da su certificado por primera vez

    class Meta:
        db_table = 'recertificacion_por_examen'
        ordering = ['-actualizado_en']


class PorExamenDocumento(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    catTiposDocumento = models.ForeignKey(CatTiposDocumento, on_delete=models.CASCADE, related_name='catTiposDocumentoPED')
    porExamen = models.ForeignKey(PorExamen, on_delete=models.CASCADE, related_name='porExamenD')
    documento = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif'])], upload_to='recertificacion')
    isAceptado = models.BooleanField(default=False, db_column='is_aceptado')

    class Meta:
        db_table = 'recertificacion_por_examen_documentos'
        ordering = ['-actualizado_en']


class RecertificacionItemDocumento(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medicoRID')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='itemRID')
    documento = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif'])], upload_to='recertificacion')
    tituloDescripcion = models.CharField(max_length=300, db_column='titulo_descripcion')
    fechaEmision = models.DateField(db_column='fecha_emision')
    puntosOtorgados = models.DecimalField(max_digits=6, decimal_places=2, db_column='puntos_otorgados')
    estatus = models.PositiveSmallIntegerField(blank=True, choices=(
        (1, 'Aceptado'),
        (2, 'Rechazado'),
        (3, 'Pendiente')
    ))
    observaciones = models.TextField(blank=True, db_column='observaciones')
    notasRechazo = models.TextField(blank=True, db_column='notas_rechzo')
    razonRechazo = models.CharField(max_length=200, blank=True, db_column='razon_rechazo')

    class Meta:
        db_table = 'recertificacion_item_documentos'
        ordering = ['-actualizado_en']


class AvanceMedicoCapitulo:
    def __init__(self, capituloDescripcion, capituloPuntos, puntosOtorgados, avance):
        self.capituloDescripcion = capituloDescripcion
        self.capituloPuntos = capituloPuntos
        self.puntosOtorgados = puntosOtorgados
        self.avance = avance


class PorcentajeGeneralMedico:
    def __init__(self, nombre, numRegistro, porcentaje, puntosObtenidos, puntosAReunir):
        self.nombre = nombre
        self.numRegistro = numRegistro
        self.porcentaje = porcentaje
        self.puntosObtenidos = puntosObtenidos
        self.puntosAReunir = puntosAReunir


class PuntosPorCapituloMedico:
    def __init__(self, titulo, descripcion, reunidos, faltantes, isExcedido, excedentes, puntosCapitulo):
        self.titulo = titulo
        self.descripcion = descripcion
        self.reunidos = reunidos
        self.faltantes = faltantes
        self.isExcedido = isExcedido
        self.excedentes = excedentes
        self.puntosCapitulo = puntosCapitulo


class Renovacion(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medicoR')
    isPagado = models.BooleanField(default=False, db_column='is_pagado')  # verificar si ya pago
    
    class Meta:
        db_table = 'recertificacion_renovaciones'
        ordering = ['-actualizado_en']