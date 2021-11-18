from django.db import models

# Create your models here.


class Institucion(models.Model):
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    nombreInstitucion = models.CharField(max_length=150, db_column='nombre_institucion')
    rfc = models.CharField(max_length=15)
    contacto = models.CharField(max_length=150)
    telUno = models.CharField(max_length=15, db_column='tel_uno')
    telDos = models.CharField(max_length=15, db_column='tel_dos')
    telCelular = models.CharField(max_length=15, db_column='tel_celular')
    email = models.CharField(max_length=50)
    pais = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    deleMuni = models.CharField(max_length=100, db_column='delegacion_municipio')
    colonia = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    cp = models.CharField(max_length=10)
    numInterior = models.CharField(max_length=10, blank=True, db_column='num_interior')
    numExterior = models.CharField(max_length=10, db_column='num_exterior')
    username = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = 'instituciones'
        ordering = ['-creado_en']
