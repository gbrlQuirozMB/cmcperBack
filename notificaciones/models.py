from django.db import models

# Create your models here.


class Notificacion(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=25, blank=True)
    mensaje = models.CharField(max_length=50, blank=True)
    destinatario = models.IntegerField()
    remitente = models.IntegerField()
    leido = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'notificacion'
        ordering = ['-creado_en']