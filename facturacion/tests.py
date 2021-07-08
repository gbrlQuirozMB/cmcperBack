from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import *
import json
from instituciones.models import *

class GetConceptoPagoListTest(APITestCase):
    def setUp(self):
        unidadMedida1 = UnidadMedida.objects.create(unidadMedida = 'UM1', nombre = 'Servicio1', descripcion = 'unidadMedida1', nota = '', simbolo = '')
        unidadMedida2 = UnidadMedida.objects.create(unidadMedida = 'UM2', nombre = 'Servicio2', descripcion = 'unidadMedida2', nota = '', simbolo = '')
        unidadMedida3 = UnidadMedida.objects.create(unidadMedida = 'UM3', nombre = 'Servicio3', descripcion = 'unidadMedida3', nota = '', simbolo = '')
        ConceptoPago.objects.create(conceptoPago = 'Pago1', precio = 100, claveSAT = 'Clave1', unidadMedida = unidadMedida1)
        ConceptoPago.objects.create(conceptoPago = 'Pago2', precio = 200, claveSAT = 'Clave2', unidadMedida = unidadMedida2)
        ConceptoPago.objects.create(conceptoPago = 'Pago3', precio = 300, claveSAT = 'Clave3', unidadMedida = unidadMedida3)
        self.user = User.objects.create_user(username = 'billy', is_staff = True)
    def test(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.get('/api/facturacion/conceptoPago/list/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetMonedaListTest(APITestCase):
    def setUp(self):
        Moneda.objects.create(moneda = 'Moneda1', descripcion = 'Descripcion1', decimales = 1, porcentajeVariacion = '1%', orden = 1)
        Moneda.objects.create(moneda = 'Moneda2', descripcion = 'Descripcion2', decimales = 2, porcentajeVariacion = '2%', orden = 2)
        Moneda.objects.create(moneda = 'Moneda3', descripcion = 'Descripcion3', decimales = 3, porcentajeVariacion = '3%', orden = 3)
        self.user = User.objects.create_user(username = 'billy', is_staff = True)
    def test(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.get('/api/facturacion/moneda/list/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetFormaPagoListTest(APITestCase):
    def setUp(self):
        FormaPago.objects.create(formaPago = 1, descripcion = 'Descripcion1', orden = 1, abreviatura = 'Abreviatura1')
        FormaPago.objects.create(formaPago = 2, descripcion = 'Descripcion2', orden = 2, abreviatura = 'Abreviatura2')
        FormaPago.objects.create(formaPago = 3, descripcion = 'Descripcion3', orden = 3, abreviatura = 'Abreviatura3')
        self.user = User.objects.create_user(username = 'billy', is_staff = True)
    def test(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.get('/api/facturacion/formaPago/list/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetUsoCFDIListTest(APITestCase):
    def setUp(self):
        UsoCFDI.objects.create(usoCFDI = 'UsoCFDI1', descripcion = 'Descripcion1', orden = 1)
        UsoCFDI.objects.create(usoCFDI = 'UsoCFDI2', descripcion = 'Descripcion2', orden = 2)
        UsoCFDI.objects.create(usoCFDI = 'UsoCFDI3', descripcion = 'Descripcion3', orden = 3)
        self.user = User.objects.create_user(username = 'billy', is_staff = True)
    def test(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.get('/api/facturacion/usoCFDI/list/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetAvalListTest(APITestCase):#Aval se refiere al modelo de Institucion
    def setUp(self):
        Institucion.objects.create(
            nombreInstitucion = 'NombreInstitucion1', rfc = 'Rfc1', contacto = 'Contacto1', telUno = 'TelUno1', telDos = 'TelDos1', telCelular = 'TelCelular1',
            email = 'Email1', pais = 'Pais1', estado = 'estado1', ciudad = 'Ciudad1', deleMuni = 'DeleMuni1', colonia = 'Colonia1', calle = 'Calle1',
            cp = 'Cp1', numInterior = 'NumInterior1', numExterior = 'NumExterior1', username = 'Username1'
        )
        Institucion.objects.create(
            nombreInstitucion = 'NombreInstitucion2', rfc = 'Rfc2', contacto = 'Contacto2', telUno = 'TelUno2', telDos = 'TelDos2', telCelular = 'TelCelular2',
            email = 'Email2', pais = 'Pais2', estado = 'estado2', ciudad = 'Ciudad2', deleMuni = 'DeleMuni2', colonia = 'Colonia2', calle = 'Calle2',
            cp = 'Cp2', numInterior = 'NumInterior2', numExterior = 'NumExterior2', username = 'Username2'
        )
        Institucion.objects.create(
            nombreInstitucion = 'NombreInstitucion3', rfc = 'Rfc3', contacto = 'Contacto3', telUno = 'TelUno3', telDos = 'TelDos3', telCelular = 'TelCelular3',
            email = 'Email3', pais = 'Pais3', estado = 'estado3', ciudad = 'Ciudad3', deleMuni = 'DeleMuni3', colonia = 'Colonia3', calle = 'Calle3',
            cp = 'Cp3', numInterior = 'NumInterior3', numExterior = 'NumExterior3', username = 'Username3'
        )
        self.user = User.objects.create_user(username = 'billy', is_staff = True)
    def test(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.get('/api/facturacion/aval/list/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)