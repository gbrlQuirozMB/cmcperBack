from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.


class Convocatoria(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualzado_en = models.DateTimeField(auto_now=True)
    fechaInicio = models.DateField(db_column='fecha_inicio')
    fechaTermino = models.DateField(db_column='fecha_termino')
    fechaExamen = models.DateField(db_column='fecha_examen')
    horaExamen = models.TimeField(db_column='hora_examen')
    nombre = models.CharField(max_length=150)
    archivo = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    banner = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'gif'])])
    detalles = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=7, decimal_places=2)
    

    class Meta:
        db_table = 'convocatoria'
        ordering = ['-creado_en']


class Sede(models.Model):
    descripcion = models.CharField(max_length=200)
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE, related_name='sedes')

    class Meta:
        db_table = 'sede'
        ordering = ['-descripcion']


class TipoExamen(models.Model):
    descripcion = models.CharField(max_length=200)
    convocatoria = models.ForeignKey(Convocatoria, on_delete=models.CASCADE, related_name='tipoExamenes')

    class Meta:
        db_table = 'tipo_examen'
        ordering = ['-descripcion']
