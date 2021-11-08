from django.db import models
from django.core.validators import FileExtensionValidator
from preregistro.models import Medico

import datetime
from dateutil.relativedelta import relativedelta

# Create your models here.


def caducidad():
    return datetime.date.today() + relativedelta(years=5)


class Certificado(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medicoC')
    documento = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif', 'jpeg'])], upload_to='certificados')
    descripcion = models.CharField(max_length=300)
    isVencido = models.BooleanField(default=False, db_column='is_vencido')  # posiblemente necesario para el cron que verifique los que ya esten evncidos y les ponga ese estatus
    fechaCertificacion = models.DateField(default=datetime.date.today, db_column='fecha_certificacion')
    fechaCaducidad = models.DateField(default=caducidad, db_column='fecha_caducidad')
    estatus = models.PositiveSmallIntegerField(blank=True, choices=(
        (1, 'Vigente'),
        (2, 'Esta por Vencer'),
        (3, 'Vencido')
    ), default=1)
    isConacem = models.BooleanField(default=False, db_column='is_tramite_concaem')  # verifica si ya esta tramitado por conacem

    class Meta:
        db_table = 'certificados'
        ordering = ['-actualizado_en']
