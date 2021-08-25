from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import *
import json, datetime
from instituciones.models import *
from preregistro.models import *

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

class GetAvalFilteredListTest(APITestCase):#Aval se refiere al modelo de Institucion
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
        response = self.client.get('/api/facturacion/aval/list/?nombreInstitucionNS=1')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetMedicoFilteredListTest(APITestCase):#Aval se refiere al modelo de Institucion
    def setUp(self):
        Medico.objects.create(
            nombre = 'Nombre1', apPaterno = 'ApPaterno1', apMaterno = 'ApMaterno1', rfcFacturacion = 'RfcFacturacion1', usoCfdi = 'P01', razonSocial = 'razonSocial1',
            telCelular = '1111111111', email = 'email1@email.com', isExtranjero = True, aceptado = True,
            estadoFisc = 'EstadoFisc1', deleMuniFisc = 'DeleMuniFisc1', coloniaFisc = 'ColoniaFisc1', calleFisc = 'CalleFisc1', cpFisc = 'CpFisc1',
            numInteriorFisc = 'NumInteriorFisc1', numExteriorFisc = 'NumExteriorFisc1',
            fechaNac = datetime.datetime.strptime('2001-01-01', '%Y-%m-%d'), fechaInicioResi = datetime.datetime.strptime('2001-01-01', '%Y-%m-%d'), fechaFinResi = datetime.datetime.strptime('2001-01-01', '%Y-%m-%d')
        )
        Medico.objects.create(
            nombre = 'Nombre2', apPaterno = 'ApPaterno2', apMaterno = 'ApMaterno2', rfcFacturacion = 'RfcFacturacion2', usoCfdi = 'P01', razonSocial = 'razonSocial2',
            telCelular = '2222222222', email = 'email2@email.com', isExtranjero = True, aceptado = True,
            estadoFisc = 'EstadoFisc2', deleMuniFisc = 'DeleMuniFisc2', coloniaFisc = 'ColoniaFisc2', calleFisc = 'CalleFisc2', cpFisc = 'CpFisc2',
            numInteriorFisc = 'NumInteriorFisc2', numExteriorFisc = 'NumExteriorFisc2',
            fechaNac = datetime.datetime.strptime('2002-02-02', '%Y-%m-%d'), fechaInicioResi = datetime.datetime.strptime('2002-02-02', '%Y-%m-%d'), fechaFinResi = datetime.datetime.strptime('2002-02-02', '%Y-%m-%d')
        )
        Medico.objects.create(
            nombre = 'Nombre3', apPaterno = 'ApPaterno3', apMaterno = 'ApMaterno3', rfcFacturacion = 'RfcFacturacion3', usoCfdi = 'G03', razonSocial = 'razonSocial3',
            telCelular = '3333333333', email = 'email3@email.com', isExtranjero = True, aceptado = True, numRegistro = 333, isCertificado = True, anioCertificacion = 2003,
            estadoFisc = 'EstadoFisc3', deleMuniFisc = 'DeleMuniFisc3', coloniaFisc = 'ColoniaFisc3', calleFisc = 'CalleFisc3', cpFisc = 'CpFisc3',
            numInteriorFisc = 'NumInteriorFisc3', numExteriorFisc = 'NumExteriorFisc3',
            fechaNac = datetime.datetime.strptime('2003-03-03', '%Y-%m-%d'), fechaInicioResi = datetime.datetime.strptime('2003-03-03', '%Y-%m-%d'), fechaFinResi = datetime.datetime.strptime('2003-03-03', '%Y-%m-%d')
        )
        Medico.objects.create(
            nombre = 'Nombre4', apPaterno = 'ApPaterno4', apMaterno = 'ApMaterno4', rfcFacturacion = 'RfcFacturacion4', usoCfdi = 'G03', razonSocial = 'razonSocial4',
            telCelular = '4444444444', email = 'email4@email.com', isExtranjero = True, aceptado = True, numRegistro = 334, isCertificado = True, anioCertificacion = 2004,
            estadoFisc = 'EstadoFisc4', deleMuniFisc = 'DeleMuniFisc4', coloniaFisc = 'ColoniaFisc4', calleFisc = 'CalleFisc4', cpFisc = 'CpFisc4',
            numInteriorFisc = 'NumInteriorFisc4', numExteriorFisc = 'NumExteriorFisc4',
            fechaNac = datetime.datetime.strptime('2004-04-04', '%Y-%m-%d'), fechaInicioResi = datetime.datetime.strptime('2004-04-04', '%Y-%m-%d'), fechaFinResi = datetime.datetime.strptime('2004-04-04', '%Y-%m-%d')
        )
        self.user = User.objects.create_user(username = 'billy', is_staff = True)
    def test(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.get('/api/facturacion/medico/list/?nombreCompletoNS=Nombre&isCertificadoNS=False')
        print(f'response JSON nombreCompleto ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/facturacion/medico/list/?rfcNS=Rfc&isCertificadoNS=False')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/api/facturacion/medico/list/?noCertificadoNS=33&isCertificadoNS=True')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetIdUltimaFacturaTest(APITestCase):
    def setUp(self):
        Factura.objects.create(codigoPostal = '01234')
        Factura.objects.create(codigoPostal = '56789')
        self.user = User.objects.create_user(username = 'billy', is_staff = True)
    def test(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.get('/api/facturacion/factura/idUltimaFactura/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')

class GetPaisListTest(APITestCase):
    def setUp(self):
        Pais.objects.create(pais = '111', descripcion = 'Descripcion1')
        Pais.objects.create(pais = '222', descripcion = 'Descripcion2')
        Pais.objects.create(pais = '333', descripcion = 'Descripcion3')
        self.user = User.objects.create_user(username = 'billy', is_staff = True)
    def test(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.get('/api/facturacion/pais/list/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class PostFacturaTest(APITestCase):
    def setUp(self):
        Institucion.objects.create(
            nombreInstitucion = 'NombreInstitucion', rfc = 'Rfc', contacto = 'Contacto', telUno = 'TelUno', telDos = 'TelDos', telCelular = 'TelCelular',
            email = 'Email', pais = 'Pais', estado = 'estado', ciudad = 'Ciudad', deleMuni = 'DeleMuni', colonia = 'Colonia', calle = 'Calle',
            cp = 'Cp', numInterior = 'NumInterior', numExterior = 'NumExterior', username = 'Username'
        )
        Medico.objects.create(
            nombre = 'Nombre', apPaterno = 'ApPaterno', apMaterno = 'ApMaterno', rfcFacturacion = 'RfcFacturacion', usoCfdi = 'G03', razonSocial = 'razonSocial',
            telCelular = '01234', email = 'email@email.com', isExtranjero = True, aceptado = True, numRegistro = 56789, isCertificado = True, anioCertificacion = 2020,
            estadoFisc = 'EstadoFisc', deleMuniFisc = 'DeleMuniFisc', coloniaFisc = 'ColoniaFisc', calleFisc = 'CalleFisc', cpFisc = 'CpFisc',
            numInteriorFisc = 'NumInteriorFisc', numExteriorFisc = 'NumExteriorFisc',
            fechaNac = datetime.datetime.strptime('1980-01-01', '%Y-%m-%d'), fechaInicioResi = datetime.datetime.strptime('2019-01-01', '%Y-%m-%d'), fechaFinResi = datetime.datetime.strptime('2020-01-01', '%Y-%m-%d')
        )
        UsoCFDI.objects.create(usoCFDI = 'UsoCFDI1', descripcion = 'Descripcion1', orden = 1)
        FormaPago.objects.create(formaPago = 1, descripcion = 'Descripcion1', orden = 1, abreviatura = 'Abreviatura1')
        Moneda.objects.create(moneda = 'Moneda1', descripcion = 'Descripcion1', decimales = 1, porcentajeVariacion = '1%', orden = 1)
        Pais.objects.create(pais = '111', descripcion = 'Descripcion1')
        unidadMedida = UnidadMedida.objects.create(unidadMedida = 'UnidadMedida', nombre = 'Nombre', descripcion = 'Descripcion', nota = 'nota', simbolo = 'Simbolo')
        ConceptoPago.objects.create(conceptoPago = 'ConceptoPago1', precio = 100, claveSAT = 'claveSAT', unidadMedida = unidadMedida)
        ConceptoPago.objects.create(conceptoPago = 'ConceptoPago2', precio = 100, claveSAT = 'claveSAT', unidadMedida = unidadMedida)
        conceptosPago = [{'idConceptoPago' : '1', 'cantidad' : '1'}, {'idConceptoPago' : '2', 'cantidad' : '1'}]
        self.json = {
            "fecha": "2021-01-01",
            "institucion  ": "1",
            #"medico ": "1",
            "usoCFDI": "1",
            "formaPago": "1",
            "moneda": "1",
            "comentarios": "Sin comentarios",
            "folio": "1",
            "subtotal": "200.00",
            "iva": "32.00",
            "total": "232.00",
            "importeLetra": "Doscientos treinta y dos pesos 00 MXN",
            "agregarDireccion": "True",
            "certificado": "2020",
            "recertificacion": "2025",
            "idPais": "1",
            "numRegIdTrib": "0123456789",
            "conceptosPago ": conceptosPago
        }
        self.user = User.objects.create_user(username = 'billy', is_staff = True)
    def test(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.post('/api/facturacion/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> 201-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, Factura.objects.count())