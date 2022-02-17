from django.db import models
from preregistro.models import Medico
from django.core.validators import FileExtensionValidator


class Carpeta(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=400, blank=True, null=True)
    # sub_carpeta = models.ForeignKey("Carpeta", blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'carpetas'
        ordering = ['nombre']


class Archivo(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    carpeta = models.ForeignKey(Carpeta, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=400, blank=True, null=True)
    archivo = models.FileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif', 'jpeg'])], upload_to='archivosCarpetas')

    class Meta:
        db_table = 'archivos'
        ordering = ['nombre']
