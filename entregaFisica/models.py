from django.db import models
from django.core.validators import FileExtensionValidator
import datetime
from preregistro.models import Medico


class CatTiposDocumentoEntrega(models.Model):
    descripcion = models.CharField(max_length=200)

    class Meta:
        db_table = 'cat_tipos_documento_entrega'
        ordering = ['descripcion']


class EntregaFisica(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    fechaEntrega = models.DateField(db_column='fecha_entrega', default=datetime.date.today)
    catTiposDocumentoEntrega = models.ForeignKey(CatTiposDocumentoEntrega, on_delete=models.SET_NULL, related_name='catTiposDocumentoEntregaEF', null=True)
    nombreRecibe = models.CharField(max_length=250, db_column='nombre_quien_recibe')
    libro = models.PositiveSmallIntegerField(blank=True, null=True)
    foja = models.PositiveSmallIntegerField(blank=True, null=True)
    archivo = models.FileField(blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'gif', 'jpeg'])], upload_to='entregaFisica')
    comentarios = models.TextField(blank=True, null=True)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='medicoEF', null=True)

    class Meta:
        db_table = 'entrega_fisica'
        ordering = ['-creado_en']
