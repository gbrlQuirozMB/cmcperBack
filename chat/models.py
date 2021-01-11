from django.db import models

# Create your models here.

class Mensaje(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    mensaje = models.CharField(max_length=300)
    destinatario = models.IntegerField()
    remitente = models.IntegerField()
    
    class Meta:
        db_table = 'mensaje'
        ordering = ['-creado_en']
        
        
class Conversacion(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=150)
    destinatario = models.IntegerField()
    
    class Meta:
        db_table = 'conversacion'
        ordering = ['-creado_en']