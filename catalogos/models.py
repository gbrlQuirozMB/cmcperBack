from django.db import models
from django.core.validators import FileExtensionValidator


# Create your models here.
class CatSedes(models.Model):
    descripcion = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    imagen = models.FileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'gif'])])

    class Meta:
        db_table = 'cat_sedes'
        ordering = ['descripcion']
        
        
class CatTiposExamen(models.Model):
    descripcion = models.CharField(max_length=200)
    
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
        (1,'Validación'),
        (2,'Engargolado')
    ))
    
    class Meta:
        db_table = 'cat_motivos_rechazo'
        ordering = ['descripcion']