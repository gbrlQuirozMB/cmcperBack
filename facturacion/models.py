from django.db import models

class FormaPago(models.Model):
    formaPago = models.IntegerField()
    descripcion = models.CharField(max_length = 100)
    orden = models.IntegerField()
    abreviatura = models.CharField(max_length = 10)
    solicitarReferencia = models.BooleanField(default = False)
    inactivo = models.BooleanField(default = False)
    class Meta:
        db_table = 'facturacionFormaPago'

class Moneda(models.Model):
    moneda = models.CharField(max_length = 100)
    descripcion = models.CharField(max_length = 100)
    decimales = models.IntegerField()
    porcentajeVariacion = models.CharField(max_length = 10)
    orden = models.IntegerField()
    inactivo = models.BooleanField(default = False)
    class Meta:
        db_table = 'facturacionMoneda'

class Pais(models.Model):
    pais = models.CharField(max_length = 100)
    descripcion = models.CharField(max_length = 100)
    formatoCodigoPostal = models.CharField(max_length = 100)
    formatoRIT = models.CharField(max_length = 100)
    validacionRIT = models.CharField(max_length = 100)
    agrupacion = models.CharField(max_length = 100)
    class Meta:
        db_table = 'facturacionPais'

class UnidadMedida(models.Model):
    unidadMedida = models.CharField(max_length = 10)
    nombre = models.CharField(max_length = 100)
    descripcion = models.CharField(max_length = 300)
    nota = models.CharField(max_length = 300)
    simbolo = models.CharField(max_length = 10)
    class Meta:
        db_table = 'facturacionUnidadMedida'

class UsoCFDI(models.Model):
    usoCFDI = models.CharField(max_length = 10)
    descripcion = models.CharField(max_length = 100)
    personaFisica = models.BooleanField(default = False)
    personaMoral = models.BooleanField(default = False)
    orden = models.IntegerField()
    inactivo = models.BooleanField(default = False)
    class Meta:
        db_table = 'facturacionUsoCFDI'

class ConceptoPago(models.Model):
    conceptoPago = models.CharField(max_length = 300)
    precio = models.IntegerField(null = True)
    inactivo = models.BooleanField(default = False)
    claveSAT = models.CharField(max_length = 50)
    unidadMedida = models.ForeignKey(UnidadMedida, on_delete = models.CASCADE, null = True)
    class Meta:
        db_table = 'facturacionConceptoPago'