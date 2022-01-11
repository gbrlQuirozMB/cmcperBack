from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import *
import json
import datetime
from instituciones.models import *
from preregistro.models import *


def configDB():
    usoCFDI1 = UsoCFDI.objects.create(usoCFDI='uso1', descripcion='USO descripcion 1', orden=1)
    usoCFDI2 = UsoCFDI.objects.create(usoCFDI='uso2', descripcion='USO descripcion 2', orden=2)
    usoCFDI3 = UsoCFDI.objects.create(usoCFDI='uso3', descripcion='USO descripcion 3', orden=3)

    moneda1 = Moneda.objects.create(moneda='Moneda1', descripcion='Descripcion 1', decimales=1, porcentajeVariacion='1%', orden=1)
    moneda2 = Moneda.objects.create(moneda='Moneda2', descripcion='Descripcion 2', decimales=2, porcentajeVariacion='2%', orden=2)
    moneda3 = Moneda.objects.create(moneda='Moneda3', descripcion='Descripcion 3', decimales=3, porcentajeVariacion='3%', orden=3)

    pais1 = Pais.objects.create(pais='pais 1', descripcion='Descripcion 1')
    pais2 = Pais.objects.create(pais='pais 2', descripcion='Descripcion 2')
    pais3 = Pais.objects.create(pais='pais 3', descripcion='Descripcion 3')

    uniMedi1 = unidadMedida = UnidadMedida.objects.create(unidadMedida='UnidadMedida 1', nombre='Nombre 1', descripcion='Descripcion 1', nota='nota 1', simbolo='Simbolo 1')
    uniMedi2 = unidadMedida = UnidadMedida.objects.create(unidadMedida='UnidadMedida 2', nombre='Nombre 2', descripcion='Descripcion 2', nota='nota 2', simbolo='Simbolo 2')
    uniMedi3 = unidadMedida = UnidadMedida.objects.create(unidadMedida='UnidadMedida 3', nombre='Nombre 3', descripcion='Descripcion 3', nota='nota 3', simbolo='Simbolo 3')

    metPago1 = MetodoPago.objects.create(metodoPago='PUE', descripcion='Pago en una sola exhibición')
    metPago2 = MetodoPago.objects.create(metodoPago='PPD', descripcion='Pago en parcialidades o diferido')

    formPago1 = FormaPago.objects.create(formaPago=1, descripcion='Efectivo', orden=1, abreviatura='EFE', solicitarReferencia=False, inactivo=False)
    formPago3 = FormaPago.objects.create(formaPago=3, descripcion='Transferencia electrónica de fondos', orden=3, abreviatura='TE', solicitarReferencia=True, inactivo=False)
    formPago4 = FormaPago.objects.create(formaPago=4, descripcion='Tarjeta de crédito', orden=4, abreviatura='TC', solicitarReferencia=True, inactivo=False)

    # -------------
    fact1 = Factura.objects.create(rfc='Rfc1', tipo='Residente', fecha='2001-01-01', hora='01:01:01', formaPago=formPago1, metodoPago=metPago1, usoCFDI=usoCFDI1,
                                   moneda=moneda1, pais=pais1, folio=1)
    fact2 = Factura.objects.create(rfc='Rfc2', tipo='Certificado', fecha='2002-02-02', hora='02:02:02', formaPago=formPago3, metodoPago=metPago2, usoCFDI=usoCFDI2,
                                   moneda=moneda2, pais=pais2, folio=2)
    fact3 = Factura.objects.create(rfc='Rfc3', tipo='Aval', fecha='2003-03-03', hora='03:03:03', formaPago=formPago4, metodoPago=metPago1, isCancelada=True, usoCFDI=usoCFDI3,
                                   moneda=moneda3, pais=pais3, folio=3)
    # -------------

    unmed1 = UnidadMedida.objects.create(unidadMedida='E48', nombre='Servicio', descripcion='descripcion1', nota='nota1', simbolo='simbolo1')
    unmed2 = UnidadMedida.objects.create(unidadMedida='H87', nombre='Pieza', descripcion='descripcion2', nota='nota2', simbolo='simbolo2')

    conPag1 = ConceptoPago.objects.create(conceptoPago='PAGO DE CERTIFICACION VIGENTE', precio=111, inactivo=False, claveSAT='sat111', unidadMedida=unmed1)
    conPag2 = ConceptoPago.objects.create(conceptoPago='PAGO EXAMEN DE CERTIFICACIÓN', precio=222, inactivo=False, claveSAT='sat222', unidadMedida=unmed1)
    conPag3 = ConceptoPago.objects.create(conceptoPago='PAGO DE EXAMEN DE CERTIFICACION VIGENTE', precio=333, inactivo=False, claveSAT='sat333', unidadMedida=unmed1)

    # -------------
    ConceptoFactura.objects.create(factura=fact1, conceptoPago=conPag1, cantidad=1)
    ConceptoFactura.objects.create(factura=fact1, conceptoPago=conPag2, cantidad=1)
    ConceptoFactura.objects.create(factura=fact2, conceptoPago=conPag1, cantidad=1)
    ConceptoFactura.objects.create(factura=fact3, conceptoPago=conPag3, cantidad=1)
    # -------------


class GetConceptoPagoListTest(APITestCase):
    def setUp(self):
        unidadMedida1 = UnidadMedida.objects.create(unidadMedida='UM1', nombre='Servicio1', descripcion='unidadMedida1', nota='', simbolo='')
        unidadMedida2 = UnidadMedida.objects.create(unidadMedida='UM2', nombre='Servicio2', descripcion='unidadMedida2', nota='', simbolo='')
        unidadMedida3 = UnidadMedida.objects.create(unidadMedida='UM3', nombre='Servicio3', descripcion='unidadMedida3', nota='', simbolo='')
        ConceptoPago.objects.create(conceptoPago='Pago1', precio=100, claveSAT='Clave1', unidadMedida=unidadMedida1)
        ConceptoPago.objects.create(conceptoPago='Pago2', precio=200, claveSAT='Clave2', unidadMedida=unidadMedida2)
        ConceptoPago.objects.create(conceptoPago='Pago3', precio=300, claveSAT='Clave3', unidadMedida=unidadMedida3)
        self.user = User.objects.create_user(username='billy', is_staff=True)

    def test(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/facturacion/conceptoPago/list/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetMonedaListTest(APITestCase):
    def setUp(self):
        Moneda.objects.create(moneda='Moneda1', descripcion='Descripcion1', decimales=1, porcentajeVariacion='1%', orden=1)
        Moneda.objects.create(moneda='Moneda2', descripcion='Descripcion2', decimales=2, porcentajeVariacion='2%', orden=2)
        Moneda.objects.create(moneda='Moneda3', descripcion='Descripcion3', decimales=3, porcentajeVariacion='3%', orden=3)
        self.user = User.objects.create_user(username='billy', is_staff=True)

    def test(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/facturacion/moneda/list/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetFormaPagoListTest(APITestCase):
    def setUp(self):
        FormaPago.objects.create(formaPago=1, descripcion='Descripcion1', orden=1, abreviatura='Abreviatura1')
        FormaPago.objects.create(formaPago=2, descripcion='Descripcion2', orden=2, abreviatura='Abreviatura2')
        FormaPago.objects.create(formaPago=3, descripcion='Descripcion3', orden=3, abreviatura='Abreviatura3')
        self.user = User.objects.create_user(username='billy', is_staff=True)

    def test(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/facturacion/formaPago/list/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetUsoCFDIListTest(APITestCase):
    def setUp(self):
        UsoCFDI.objects.create(usoCFDI='UsoCFDI1', descripcion='Descripcion1', orden=1)
        UsoCFDI.objects.create(usoCFDI='UsoCFDI2', descripcion='Descripcion2', orden=2)
        UsoCFDI.objects.create(usoCFDI='UsoCFDI3', descripcion='Descripcion3', orden=3)
        self.user = User.objects.create_user(username='billy', is_staff=True)

    def test(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/facturacion/usoCFDI/list/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAvalFilteredListTest(APITestCase):  # Aval se refiere al modelo de Institucion
    def setUp(self):
        Institucion.objects.create(
            nombreInstitucion='NombreInstitucion1', rfc='Rfc1', contacto='Contacto1', telUno='TelUno1', telDos='TelDos1', telCelular='TelCelular1',
            email='Email1', pais='Pais1', estado='estado1', ciudad='Ciudad1', deleMuni='DeleMuni1', colonia='Colonia1', calle='Calle1',
            cp='Cp1', numInterior='NumInterior1', numExterior='NumExterior1', username='Username1'
        )
        Institucion.objects.create(
            nombreInstitucion='NombreInstitucion2', rfc='Rfc2', contacto='Contacto2', telUno='TelUno2', telDos='TelDos2', telCelular='TelCelular2',
            email='Email2', pais='Pais2', estado='estado2', ciudad='Ciudad2', deleMuni='DeleMuni2', colonia='Colonia2', calle='Calle2',
            cp='Cp2', numInterior='NumInterior2', numExterior='NumExterior2', username='Username2'
        )
        Institucion.objects.create(
            nombreInstitucion='NombreInstitucion3', rfc='Rfc3', contacto='Contacto3', telUno='TelUno3', telDos='TelDos3', telCelular='TelCelular3',
            email='Email3', pais='Pais3', estado='estado3', ciudad='Ciudad3', deleMuni='DeleMuni3', colonia='Colonia3', calle='Calle3',
            cp='Cp3', numInterior='NumInterior3', numExterior='NumExterior3', username='Username3'
        )
        self.user = User.objects.create_user(username='billy', is_staff=True)

    def test(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/facturacion/aval/list/?nombreInstitucionNS=1')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetMedicoFilteredListTest(APITestCase):  # Aval se refiere al modelo de Institucion
    def setUp(self):
        Medico.objects.create(
            nombre='Nombre1', apPaterno='ApPaterno1', apMaterno='ApMaterno1', rfcFacturacion='RfcFacturacion1', usoCfdi='P01', razonSocial='razonSocial1', telCelular='1111111111',
            email='email1@email.com', isExtranjero=True, aceptado=True, estadoFisc='EstadoFisc1', deleMuniFisc='DeleMuniFisc1', coloniaFisc='ColoniaFisc1', calleFisc='CalleFisc1', cpFisc='CpFisc1',
            numInteriorFisc='NumInteriorFisc1', numExteriorFisc='NumExteriorFisc1', fechaNac=datetime.datetime.strptime('2001-01-01', '%Y-%m-%d'),
            fechaInicioResi=datetime.datetime.strptime('2001-01-01', '%Y-%m-%d'),
            fechaFinResi=datetime.datetime.strptime('2001-01-01', '%Y-%m-%d'))
        Medico.objects.create(
            nombre='Nombre2', apPaterno='ApPaterno2', apMaterno='ApMaterno2', rfcFacturacion='RfcFacturacion2', usoCfdi='P01', razonSocial='razonSocial2', telCelular='2222222222',
            email='email2@email.com', isExtranjero=True, aceptado=True, estadoFisc='EstadoFisc2', deleMuniFisc='DeleMuniFisc2', coloniaFisc='ColoniaFisc2', calleFisc='CalleFisc2', cpFisc='CpFisc2',
            numInteriorFisc='NumInteriorFisc2', numExteriorFisc='NumExteriorFisc2', fechaNac=datetime.datetime.strptime('2002-02-02', '%Y-%m-%d'),
            fechaInicioResi=datetime.datetime.strptime('2002-02-02', '%Y-%m-%d'),
            fechaFinResi=datetime.datetime.strptime('2002-02-02', '%Y-%m-%d'))
        Medico.objects.create(
            nombre='Nombre3', apPaterno='ApPaterno3', apMaterno='ApMaterno3', rfcFacturacion='RfcFacturacion3', usoCfdi='G03', razonSocial='razonSocial3', telCelular='3333333333',
            email='email3@email.com', isExtranjero=True, aceptado=True, numRegistro=333, isCertificado=True, anioCertificacion=2003, estadoFisc='EstadoFisc3', deleMuniFisc='DeleMuniFisc3',
            coloniaFisc='ColoniaFisc3', calleFisc='CalleFisc3', cpFisc='CpFisc3', numInteriorFisc='NumInteriorFisc3', numExteriorFisc='NumExteriorFisc3', fechaNac=datetime.datetime.strptime(
                '2003-03-03', '%Y-%m-%d'),
            fechaInicioResi=datetime.datetime.strptime('2003-03-03', '%Y-%m-%d'),
            fechaFinResi=datetime.datetime.strptime('2003-03-03', '%Y-%m-%d'))
        Medico.objects.create(
            nombre='Nombre4', apPaterno='ApPaterno4', apMaterno='ApMaterno4', rfcFacturacion='RfcFacturacion4', usoCfdi='G03', razonSocial='razonSocial4', telCelular='4444444444',
            email='email4@email.com', isExtranjero=True, aceptado=True, numRegistro=334, isCertificado=True, anioCertificacion=2004, estadoFisc='EstadoFisc4', deleMuniFisc='DeleMuniFisc4',
            coloniaFisc='ColoniaFisc4', calleFisc='CalleFisc4', cpFisc='CpFisc4', numInteriorFisc='NumInteriorFisc4', numExteriorFisc='NumExteriorFisc4', fechaNac=datetime.datetime.strptime(
                '2004-04-04', '%Y-%m-%d'),
            fechaInicioResi=datetime.datetime.strptime('2004-04-04', '%Y-%m-%d'),
            fechaFinResi=datetime.datetime.strptime('2004-04-04', '%Y-%m-%d'))
        self.user = User.objects.create_user(username='billy', is_staff=True)

    def test(self):
        self.client.force_authenticate(user=self.user)
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
        Factura.objects.create(codigoPostal='01234')
        Factura.objects.create(codigoPostal='56789')
        self.user = User.objects.create_user(username='billy', is_staff=True)

    def test(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/facturacion/factura/idUltimaFactura/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')


class GetPaisListTest(APITestCase):
    def setUp(self):
        Pais.objects.create(pais='111', descripcion='Descripcion1')
        Pais.objects.create(pais='222', descripcion='Descripcion2')
        Pais.objects.create(pais='333', descripcion='Descripcion3')
        self.user = User.objects.create_user(username='billy', is_staff=True)

    def test(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/facturacion/pais/list/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostFacturaTest(APITestCase):
    def setUp(self):
        """ Institucion.objects.create(
            nombreInstitucion = 'NombreInstitucion', rfc = 'Rfc', contacto = 'Contacto', telUno = 'TelUno', telDos = 'TelDos', telCelular = 'TelCelular',
            email = 'Email', pais = 'Pais', estado = 'estado', ciudad = 'Ciudad', deleMuni = 'DeleMuni', colonia = 'Colonia', calle = 'Calle',
            cp = 'Cp', numInterior = 'NumInterior', numExterior = 'NumExterior', username = 'Username'
        ) """
        Medico.objects.create(
            nombre='Nombre', apPaterno='ApPaterno', apMaterno='ApMaterno', rfcFacturacion='EKU9003173C9', usoCfdi='G03', razonSocial='RazonSocial', telCelular='01234', email='email@email.com',
            isExtranjero=True, aceptado=True, numRegistro=56789, isCertificado=True, anioCertificacion=2020, estadoFisc='EstadoFisc', deleMuniFisc='DeleMuniFisc', coloniaFisc='ColoniaFisc',
            calleFisc='CalleFisc', cpFisc='42080', numInteriorFisc='NumInteriorFisc', numExteriorFisc='NumExteriorFisc', fechaNac=datetime.datetime.strptime('1980-01-01', '%Y-%m-%d'),
            fechaInicioResi=datetime.datetime.strptime('2019-01-01', '%Y-%m-%d'),
            fechaFinResi=datetime.datetime.strptime('2020-01-01', '%Y-%m-%d'))
        usoCFDI3 = UsoCFDI.objects.create(usoCFDI='G03', descripcion='Descripcion1', orden=1)
        formPago4 = FormaPago.objects.create(formaPago=1, descripcion='Descripcion1', orden=1, abreviatura='Abreviatura1')
        metPago1 = MetodoPago.objects.create(metodoPago='PUE', descripcion='Pago en una sola exhibición')
        moneda3 = Moneda.objects.create(moneda='MXN', descripcion='Descripcion1', decimales=1, porcentajeVariacion='1%', orden=1)
        pais3 = Pais.objects.create(pais='111', descripcion='Descripcion1')
        unidadMedida = UnidadMedida.objects.create(unidadMedida='E48', nombre='Nombre', descripcion='Descripcion', nota='nota', simbolo='Simbolo')
        ConceptoPago.objects.create(conceptoPago='ConceptoPago1', precio=100, claveSAT='10101500', unidadMedida=unidadMedida)
        ConceptoPago.objects.create(conceptoPago='ConceptoPago2', precio=100, claveSAT='10101500', unidadMedida=unidadMedida)
        # para probar cuado ya existe un factura tome el FOLIO correcto
        # fact3 = Factura.objects.create(rfc='Rfc3', tipo='Aval', fecha='2003-03-03', hora='03:03:03', formaPago=formPago4, metodoPago=metPago1, isCancelada=True, usoCFDI=usoCFDI3,
        #                            moneda=moneda3, pais=pais3, folio=3)
        conceptosPago = [{'idConceptoPago': '1', 'cantidad': '1'}, {'idConceptoPago': '2', 'cantidad': '1'}]
        self.json = {

            # "institucion": "1",
            "medico": "1",
            "usoCFDI": 1,
            "formaPago": 1,
            "moneda": 1,
            "pais": 1,
            "metodoPago": 1,
            "comentarios": "Sin comentarios",
            # "folio": "1",  # este no debe ir, se toma del ultimo registro existente en la tabla
            "subtotal": 200.00,
            "iva": 32.00,
            "total": 232.00,
            "numRegIdTrib": "0123456789",
            "importeLetra": "Doscientos treinta y dos pesos 00 MXN",
            "agregarDireccion": True,
            "certificado": "2020",
            "recertificacion": "2025",
            "conceptosPago": conceptosPago,
            # "fecha": "1999-09-09",
            "fecha": "2022-01-10T09:06:03",
            # "fecha": datetime.datetime.now(),
            # "hora": "03:33:33",
            "tipo": "Aval",
            # "codigoPostal": "21397",

        }
        self.user = User.objects.create_user(username='billy', is_staff=True)

    def test(self):

        print(f'--->>>json: {self.json}')

        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/facturacion/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> 201-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetFacturaFilteredListTest(APITestCase):
    def setUp(self):
        configDB()

        self.user = User.objects.create_user(username='billy', is_staff=True)

    def test(self):
        self.client.force_authenticate(user=self.user)

        # response = self.client.get('/api/facturacion/list/?tipo=Aval')
        # print(f'response JSON ===>>> filtrado por tipo=Aval \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/facturacion/list/?fechaInicioNS=2002-02-02&fechaFinNS=2003-03-03')
        # print(f'response JSON ===>>> filtrado por rango de fechas \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/facturacion/list/?concepto=1')
        # print(f'response JSON ===>>> filtrado por concepto=1 \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/facturacion/list/?isCancelada=false')
        # print(f'response JSON ===>>> filtrado por isCancelada=false \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/facturacion/list/?formaPago=3')
        # print(f'response JSON ===>>> formaPago=3 \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/facturacion/list/?metodoPago=1')
        # print(f'response JSON ===>>> metodoPago=2 \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/facturacion/list/?rfcNS=Rfc3')
        print(f'response JSON ===>>> rfcNS=Rfc1 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostFacturaCancelarTest(APITestCase):
    def setUp(self):
        Factura.objects.create()
        Factura.objects.create()
        Factura.objects.create()
        self.json = {
            "id": "1"
        }
        self.user = User.objects.create_user(username='billy', is_staff=True)

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = Factura.objects.get(id=1)
        print(f'\n--->>>isCancelada: {dato.isCancelada}')

        response = self.client.post('/api/facturacion/cancelar/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        try:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        except:
            self.assertEqual(response.status_code, status.HTTP_417_EXPECTATION_FAILED)

        dato = Factura.objects.get(id=1)
        print(f'\n--->>>isCancelada: {dato.isCancelada}')


class GetFacturaFilteredListDownExcelTest(APITestCase):
    def setUp(self):
        configDB()

        self.user = User.objects.create_user(username='billy', is_staff=True)

    def test(self):
        self.client.force_authenticate(user=self.user)

        # response = self.client.get('/api/facturacion/bajar-excel/list/?tipo=Aval')
        # print(f'response JSON ===>>> filtrado por tipo=Aval \n {response.content} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/facturacion/bajar-excel/list/?fechaInicioNS=2002-02-02&fechaFinNS=2003-03-03')
        print(f'response JSON ===>>> filtrado por rango de fechas \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/facturacion/bajar-excel/list/?concepto=1')
        # print(f'response JSON ===>>> filtrado por concepto=1 \n {response.content} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/facturacion/bajar-excel/list/?isCancelada=false')
        # print(f'response JSON ===>>> filtrado por isCancelada=false \n {response.content} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/facturacion/bajar-excel/list/?formaPago=3')
        # print(f'response JSON ===>>> formaPago=3 \n {response.content} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/facturacion/bajar-excel/list/?metodoPago=1')
        # print(f'response JSON ===>>> metodoPago=2 \n {response.content} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/facturacion/bajar-excel/list/?rfcNS=Rfc3')
        # print(f'response JSON ===>>> rfcNS=Rfc1 \n {response.content} \n ---')
        # # print(f'response JSON ===>>> rfcNS=Rfc1 \n {response} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetMetodoPagoListTest(APITestCase):
    def setUp(self):
        MetodoPago.objects.create(metodoPago='PUE', descripcion='Pago en una sola exhibición')
        MetodoPago.objects.create(metodoPago='PPD', descripcion='Pago en parcialidades o diferido')

        self.user = User.objects.create_user(username='billy', is_staff=True)

    def test(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/facturacion/metodo-pago/list/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OtrosTest(APITestCase):
    def setUp(self):
        configDB()

    def test(self):
        for dato in Factura.objects.filter():
            print(f'id: {dato.id} - creado_en: {dato.creado_en} - folio: {dato.folio}')

        dato = Factura.objects.filter()[:1]
        if dato.get().folio is None:
            print(f'dato: 1')
        else:
            print(f'dato: {dato.get().folio}')
            valor = int(dato.get().folio)
            valor += 1
            print(f'valor: {valor}')


# ******************** CRUD de concepto de pago ********************

def configCatalogosDB():
    unmed1 = UnidadMedida.objects.create(unidadMedida='E48', nombre='Servicio', descripcion='descripcion1', nota='nota1', simbolo='simbolo1')
    unmed2 = UnidadMedida.objects.create(unidadMedida='H87', nombre='Pieza', descripcion='descripcion2', nota='nota2', simbolo='simbolo2')

    ConceptoPago.objects.create(conceptoPago='PAGO DE CERTIFICACION VIGENTE', precio=111, inactivo=False, claveSAT='sat111', unidadMedida=unmed1)
    ConceptoPago.objects.create(conceptoPago='PAGO EXAMEN DE CERTIFICACIÓN', precio=222, inactivo=False, claveSAT='sat222', unidadMedida=unmed1)
    ConceptoPago.objects.create(conceptoPago='PAGO DE EXAMEN DE CERTIFICACION VIGENTE', precio=333, inactivo=False, claveSAT='sat333', unidadMedida=unmed1)

    FormaPago.objects.create(formaPago=1, descripcion='Efectivo', orden=1, abreviatura='EFE', solicitarReferencia=False, inactivo=False)
    FormaPago.objects.create(formaPago=3, descripcion='Transferencia electrónica de fondos', orden=3, abreviatura='TE', solicitarReferencia=True, inactivo=False)
    FormaPago.objects.create(formaPago=4, descripcion='Tarjeta de crédito', orden=4, abreviatura='TC', solicitarReferencia=True, inactivo=False)

    Moneda.objects.create(moneda='Moneda1', descripcion='Descripcion 1', decimales=1, porcentajeVariacion='1%', orden=1)
    Moneda.objects.create(moneda='Moneda2', descripcion='Descripcion 2', decimales=2, porcentajeVariacion='2%', orden=2)
    Moneda.objects.create(moneda='Moneda3', descripcion='Descripcion 3', decimales=3, porcentajeVariacion='3%', orden=3)

    UsoCFDI.objects.create(usoCFDI='uso1', descripcion='USO descripcion 1', orden=1)
    UsoCFDI.objects.create(usoCFDI='uso2', descripcion='USO descripcion 2', orden=2)
    UsoCFDI.objects.create(usoCFDI='uso3', descripcion='USO descripcion 3', orden=3)


class CuConceptoPagoTest(APITestCase):
    def setUp(self):

        configCatalogosDB()

        self.json = {
            "conceptoPago": "conceptoPago 4",
            "precio": 444,
            "inactivo": True,
            "claveSAT": "sat444",
            "unidadMedida": 2
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/facturacion/concepto-pago/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> concepto-pago OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put('/api/facturacion/concepto-pago/1/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> concepto-pago OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get('/api/facturacion/conceptoPago/list/')
        print(f'response JSON ===>>> concepto-pago OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get('/api/facturacion/conceptoPago/list/?inactivo=true')
        print(f'response JSON ===>>> concepto-pago OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CuFormaPagoTest(APITestCase):
    def setUp(self):

        configCatalogosDB()

        self.json = {
            "formaPago": 2,
            "descripcion": "formaPago2",
            "orden": 2,
            "abreviatura": "FP2",
            "solicitarReferencia": False,
            "inactivo": False,
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/facturacion/forma-pago/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> concepto-pago OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put('/api/facturacion/forma-pago/1/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> concepto-pago OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CuMonedaTest(APITestCase):
    def setUp(self):

        configCatalogosDB()

        self.json = {
            "moneda": "moneda4",
            "descripcion": "descripcion4",
            "decimales": 4,
            "tipoCambio": 4,
            "porcentajeVariacion": "4%",
            "orden": 4,
            "inactivo": False,
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/facturacion/moneda/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> concepto-pago OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put('/api/facturacion/moneda/1/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> concepto-pago OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CuUsoCFDITest(APITestCase):
    def setUp(self):

        configCatalogosDB()

        self.json = {
            "usoCFDI": "uso4",
            "descripcion": "descripcion4",
            "personaFisica": True,
            "personaMoral": True,
            "orden": 4,
            "inactivo": True,
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/facturacion/uso-cfdi/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> concepto-pago OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put('/api/facturacion/uso-cfdi/1/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> concepto-pago OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
