from django.db import models
from django.core.validators import FileExtensionValidator
from preregistro.models import Medico

import datetime
from dateutil.relativedelta import relativedelta

# Create your models here.


class Conacem(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    fechaEnvio = models.DateField(default=datetime.date.today, db_column='fecha_envio')
    tituloPresidente = models.CharField(max_length=10, db_column='titulo_presidente')
    nombrePresidente = models.CharField(max_length=200, db_column='nombre_presidente')
    tituloResponsable = models.CharField(max_length=10, db_column='titulo_responsable')
    nombreResponsable = models.CharField(max_length=200, db_column='nombre_responsable')
    fechaEmision = models.DateField(default=datetime.date.today, db_column='fecha_emision')
    costo = models.DecimalField(max_digits=7, decimal_places=2, null=True, default=0)
    fechaValidezDel = models.DateField(default=datetime.date.today, db_column='fecha_validez_del')
    fechaValidezAl = models.DateField(default=datetime.date.today, db_column='fecha_validez_al')
    iniciaLibro = models.PositiveSmallIntegerField(db_column='inicia_libro')
    hoja = models.PositiveSmallIntegerField(db_column='hoja')
    lugar = models.PositiveSmallIntegerField(db_column='lugar')
    cupo = models.PositiveSmallIntegerField(db_column='cupo')

    class Meta:
        db_table = 'conacem'
        ordering = ['-actualizado_en']


class DetalleConcacem(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medico')
    conacem = models.ForeignKey(Conacem, on_delete=models.CASCADE, related_name='medicos')
    libro = models.PositiveSmallIntegerField(blank=True, null=True, db_column='libro')
    foja = models.PositiveSmallIntegerField(blank=True, null=True, db_column='foja')
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'detalles_conacem'
        ordering = ['-actualizado_en']
