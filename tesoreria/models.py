from django.db import models
from preregistro.models import Medico
from instituciones.models import Institucion

from django.core.validators import FileExtensionValidator

# Create your models here.

class Pago(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, null=True, related_name='medicoP')
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=True, related_name='institucionP')
    concepto = models.CharField(max_length=400, blank=True)
    comprobante = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif', 'jpeg'])], upload_to='tesoreria')
    monto = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    nota = models.CharField(max_length=400, blank=True)
    estatus = models.PositiveSmallIntegerField(blank=True, choices=(
        (1, 'Aceptado'),
        (2, 'Rechazado'),
        (3, 'Pendiente')
    ))
    tipo = models.PositiveSmallIntegerField(blank=True)
    externoId = models.IntegerField(blank=True, null=True)
    numeroPago = models.PositiveSmallIntegerField(default=1, db_column='numero_pago')

    class Meta:
        db_table = 'registros_pagos'
        ordering = ['-actualizado_en']