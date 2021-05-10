from django.db import models
from django.core.validators import FileExtensionValidator


# Create your models here.
class Comunicado(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    titulo = models.CharField(max_length=300)
    categoria = models.PositiveSmallIntegerField(blank=True, choices=(
        (1, 'Categoria 1'),
        (2, 'Categoria 2'),
        (3, 'Categoria 3')
    ))
    imagen = models.FileField(blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'png', 'jpg', 'gif'])])
    detalles = models.TextField(blank=True)
    isActivo = models.BooleanField(default=False, db_column='is_activo')  # si se utiliza o no

    class Meta:
        db_table = 'comunicados'
        ordering = ['-actualizado_en']