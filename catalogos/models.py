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
