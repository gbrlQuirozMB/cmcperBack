from django.db import models
from django.core.validators import FileExtensionValidator

from instituciones.models import Institucion
from recertificacion.models import Item


# Create your models here.
class ActividadAvalada(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, related_name='institucionA')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='itemA')
    nombre = models.CharField(max_length=200)
    emailContacto = models.CharField(max_length=50, db_column='email_contacto')
    archivo = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    banner = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'gif'])])
    numAsistentes = models.PositiveSmallIntegerField(db_column='numero_asistentes')
    puntosAsignar = models.DecimalField(max_digits=6, decimal_places=2, db_column='puntos_asignar')
    fechaInicio = models.DateField(db_column='fecha_inicio')
    lugar = models.CharField(max_length=300)
    solicitante = models.CharField(max_length=300)
    tipoPago = models.PositiveSmallIntegerField(db_column='tipo_pago', choices=(
        (1, 'Porcentaje'),
        (2, 'Precio'),
    ))
    porcentaje = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    precio = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        db_table = 'actividades_avaladas'
        ordering = ['-creado_en']


class Tema(models.Model):
    nombre = models.CharField(max_length=300)
    actividadAvalada = models.ForeignKey(ActividadAvalada, on_delete=models.CASCADE, related_name='actividadAvaladaT')

    class Meta:
        db_table = 'temas'
        ordering = ['-nombre']