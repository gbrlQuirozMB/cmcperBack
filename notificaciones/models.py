from django.db import models

# Create your models here.


class Notificacion(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=50, blank=True)
    mensaje = models.CharField(max_length=50, blank=True)
    destinatario = models.IntegerField(blank=True, null=True)
    remitente = models.IntegerField(blank=True, null=True)
    leido = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'notificacion'
        ordering = ['-creado_en']