from django.db import models
from instituciones.models import *
from preregistro.models import *
import os

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
    tipoCambio = models.IntegerField(default = 1)
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
    unidadMedida = models.ForeignKey(UnidadMedida, on_delete = models.SET_NULL, null = True)
    class Meta:
        db_table = 'facturacionConceptoPago'

def rutaTimbrado(instance, nombreArchivo):
    rfc = ''
    if instance.institucion:
        rfc = instance.institucion.rfc
    else:
        rfc = instance.medico.rfc
    return os.path.join('facturasTimbradas/', rfc, instance.fecha.date().strftime("%d-%m-%Y"), nombreArchivo)
def rutaCancelado(instance, nombreArchivo):
    rfc = ''
    if instance.institucion:
        rfc = instance.institucion.rfc
    else:
        rfc = instance.medico.rfc
    return os.path.join('facturasCanceladas/', rfc, instance.fecha.date().strftime("%d-%m-%Y"), nombreArchivo)

class Factura(models.Model):
    fecha = models.DateTimeField(auto_now = True)
    institucion = models.ForeignKey(Institucion, on_delete = models.SET_NULL, null = True)
    medico = models.ForeignKey(Medico, on_delete = models.SET_NULL, null = True)
    rfc = models.CharField(max_length = 150, null = True)
    razonSocial = models.CharField(max_length = 150, null = True)
    estado = models.CharField(max_length = 150, null = True)
    deleMuni = models.CharField(max_length = 150, null = True)
    colonia = models.CharField(max_length = 150, null = True)
    calle = models.CharField(max_length = 150, null = True)
    numInterior = models.CharField(max_length = 150, null = True)
    numExterior = models.CharField(max_length = 150, null = True)
    codigoPostal = models.CharField(max_length = 150, null = True)
    usoCFDI = models.ForeignKey(UsoCFDI, on_delete = models.SET_NULL, null = True)
    formaPago = models.ForeignKey(FormaPago, on_delete = models.SET_NULL, null = True)
    moneda = models.ForeignKey(Moneda, on_delete = models.SET_NULL, null = True)
    comentarios = models.CharField(max_length = 250, null = True, blank = True)
    folio = models.CharField(max_length = 50, null = True)
    subtotal = models.DecimalField(decimal_places = 6, max_digits = 21, null = True)
    iva = models.DecimalField(decimal_places = 6, max_digits = 21, null = True)
    total = models.DecimalField(decimal_places = 6, max_digits = 21, null = True)
    pais = models.ForeignKey(Pais, on_delete = models.SET_NULL, null = True)
    numRegIdTrib = models.CharField(max_length = 50, null = True)
    uuid = models.CharField(max_length = 50, null = True)
    cadenaOriginal = models.TextField(null = True)
    numeroCertificado = models.CharField(max_length = 50,  null = True)
    numeroCertificadoSAT = models.CharField(max_length = 50,  null = True)
    selloSAT = models.TextField(null = True)
    selloCFDI = models.TextField(null = True)
    fechaTimbrado = models.DateTimeField(null = True)
    fechaCancelado = models.DateTimeField(null = True)
    xmlTimbrado = models.FileField(upload_to = rutaTimbrado, null = True)
    xmlCancelado = models.FileField(upload_to = rutaCancelado, null = True)
    pdf = models.CharField(max_length = 500, null = True)
    class Meta:
        db_table = 'facturacionFactura'

class ConceptoFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete = models.CASCADE)
    conceptoPago = models.ForeignKey(ConceptoPago, on_delete = models.CASCADE)
    cantidad = models.IntegerField()
    class Meta:
        db_table = 'facturacionConceptoFactura'