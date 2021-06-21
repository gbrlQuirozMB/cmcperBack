from django.db import models

class FormaPago(models.Model):
    formaPago = models.IntegerField()
    descripcion = models.CharField(max_length = 100)
    orden = models.IntegerField()
    abreviatura = models.CharField(max_length = 10)
    solicitarReferencia = models.BooleanField(default = False)
    inactivo = models.BooleanField(default = False)
    class Meta:
        db_table = 'formaPago'

class Moneda(models.Model):
    moneda = models.CharField(max_length = 100)
    descripcion = models.CharField(max_length = 100)
    decimales = models.IntegerField()
    porcentajeVariacion = models.CharField(max_length = 10)
    orden = models.IntegerField()
    inactivo = models.BooleanField(default = False)
    class Meta:
        db_table = 'moneda'

class Pais(models.Model):
    pais = models.CharField(max_length = 100)
    descripcion = models.CharField(max_length = 100)
    formatoCodigoPostal = models.CharField(max_length = 100)
    formatoRIT = models.CharField(max_length = 100)
    validacionRIT = models.CharField(max_length = 100)
    agrupacion = models.CharField(max_length = 100)
    class Meta:
        db_table = 'pais'

class UnidadMedida(models.Model):
    unidadMedida = models.CharField(max_length = 10)
    nombre = models.CharField(max_length = 100)
    descripcion = models.CharField(max_length = 300)
    nota = models.CharField(max_length = 300)
    simbolo = models.CharField(max_length = 10)
    class Meta:
        db_table = 'unidadMedida'

class UsoCFDI(models.Model):
    usoCFDI = models.CharField(max_length = 10)
    descripcion = models.CharField(max_length = 100)
    personaFisica = models.BooleanField(default = False)
    personaMoral = models.BooleanField(default = False)
    orden = models.IntegerField()
    inactivo = models.BooleanField(default = False)
    class Meta:
        db_table = 'usoCFDI'