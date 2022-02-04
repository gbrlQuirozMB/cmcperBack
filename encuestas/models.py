from django.db import models
import datetime
from preregistro.models import Medico


class Encuesta(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    titulo = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=200)
    fechaInicio = models.DateField(db_column='fecha_inicio', default=datetime.date.today)
    fechaFin = models.DateField(db_column='fecha_fin', default=datetime.date.today)
    estatus = models.CharField(max_length=15, choices=(
        ('Editar', 'Editar'),
        ('Abierta', 'Abierta'),
        ('Cerrada', 'Cerrada')
    ), default="Editar")
    regionGeografica = models.CharField(max_length=300, blank=True, null=True, db_column='region_geografica')
    isSoloConsejero = models.BooleanField(default=False, db_column='is_solo_consejero')

    class Meta:
        db_table = 'encuestas'
        ordering = ['-creado_en']


class Pregunta(models.Model):
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    orden = models.PositiveSmallIntegerField()
    hasOtro = models.BooleanField(default=False, db_column='acepta_otro')

    class Meta:
        db_table = 'preguntas'
        ordering = ['orden']


class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    orden = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'opciones'
        ordering = ['orden']


class Respuesta(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    opcion = models.ForeignKey(Opcion, on_delete=models.SET_NULL, null=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    fecha = models.DateField(default=datetime.date.today)
    otro = models.CharField(max_length=200, blank=True, null=True)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)

    class Meta:
        db_table = 'respuestas'
        ordering = ['-creado_en']
