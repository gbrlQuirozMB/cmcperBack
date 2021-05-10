from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


from preregistro.models import Medico
from recertificacion.models import *

from django.db.models import Sum

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from django.utils import timezone
import datetime

from django.db.models import Q

from notificaciones.models import Notificacion
from certificados.models import Certificado


# Create your tests here.
class GetCertificadoDatos200Test(APITestCase):
    def setUp(self):
        medico1 = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=369)

        Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=False, fechaCertificacion='2021-04-06',
                                   fechaCaducidad='2026-04-06', estatus=1)
        Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=True, fechaCertificacion='2000-04-06',
                                   fechaCaducidad='2005-04-06', estatus=3)
        Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=True, fechaCertificacion='2016-05-06',
                                   fechaCaducidad='2021-05-06', estatus=1)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/medico/1/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        Certificado.objects.filter(id=3).update(fechaCertificacion='2000-04-06', fechaCaducidad='2005-04-06', estatus=3)  # para revisar que esta vigente
        response = self.client.get('/api/recertificacion/medico/1/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        Certificado.objects.filter(id=3).update(fechaCertificacion='2016-05-06', fechaCaducidad='2021-05-06', estatus=2)  # para revisar que esta por vencer
        response = self.client.get('/api/recertificacion/medico/1/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/medico/11/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAvanceMedicoCapitulo200Test(APITestCase):
    def setUp(self):
        medico1 = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=369)

        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=50.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)
        item2 = Item.objects.create(descripcion='item descripcion 2', puntos=6, subcapitulo=subcapitulo1)
        item3 = Item.objects.create(descripcion='item descripcion 3', puntos=9, subcapitulo=subcapitulo1)

        RecertificacionItemDocumento.objects.create(medico=medico1, item=item1, documento='doc1.pdf', tituloDescripcion='tituloDescripcion 1', fechaEmision='2021-04-06', puntosOtorgados=3.0,
                                                    estatus=1, observaciones='observaciones 1', notasRechazo='notasRechazo 1', razonRechazo='razonRechazo 1')
        RecertificacionItemDocumento.objects.create(medico=medico1, item=item1, documento='doc2.pdf', tituloDescripcion='tituloDescripcion 2', fechaEmision='2022-04-06', puntosOtorgados=6.0,
                                                    estatus=1, observaciones='observaciones 2', notasRechazo='notasRechazo 2', razonRechazo='razonRechazo 2')
        RecertificacionItemDocumento.objects.create(medico=medico1, item=item1, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=9.0,
                                                    estatus=2, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/medico/1/capitulo/1/avance/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/medico/1/capitulo/2/avance/')
        print(f'response JSON ===>>> capitulo no encontrado \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get('/api/recertificacion/medico/2/capitulo/1/avance/')
        print(f'response JSON ===>>> medico no encontrado \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # # prueba del filtro
        # cuenta = RecertificacionItemDocumento.objects.filter(medico=1, item__subcapitulo__capitulo=1, estatus=1).count()
        # print(f'--->>>cuenta: {cuenta}')
        # # prueba de la sumatoria de los puntos
        # suma = RecertificacionItemDocumento.objects.filter(medico=1, item__subcapitulo__capitulo=1, estatus=1).aggregate(Sum('puntosOtorgados'))
        # print(f'--->>>suma: {suma}')


class GetPuntosCapituloList200Test(APITestCase):
    def setUp(self):
        medico1 = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=369)

        Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=30.0, maximo=50.0, minimo=50.0, isOpcional=False)
        Capitulo.objects.create(titulo='titulo 2', descripcion='capitulo descripcion 2', puntos=60.0, maximo=60.0, minimo=60.0, isOpcional=False)
        Capitulo.objects.create(titulo='titulo 3', descripcion='capitulo descripcion 3', puntos=90.0, maximo=90.0, minimo=90.0, isOpcional=True)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/puntos-capitulo/list/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetPuntosCapituloDetail200Test(APITestCase):
    def setUp(self):
        medico1 = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=369)

        Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=30.0, maximo=50.0, minimo=50.0, isOpcional=False)
        Capitulo.objects.create(titulo='titulo 2', descripcion='capitulo descripcion 2', puntos=60.0, maximo=60.0, minimo=60.0, isOpcional=False)
        Capitulo.objects.create(titulo='titulo 3', descripcion='capitulo descripcion 3', puntos=90.0, maximo=90.0, minimo=90.0, isOpcional=True)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/puntos-capitulo/3/detail/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/puntos-capitulo/33/detail/')
        print(f'response JSON ===>>> no encontrado \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetPorcentajeGeneralMedico200Test(APITestCase):
    def setUp(self):
        medico1 = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=369)

        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)
        item2 = Item.objects.create(descripcion='item descripcion 2', puntos=6, subcapitulo=subcapitulo1)
        item3 = Item.objects.create(descripcion='item descripcion 3', puntos=9, subcapitulo=subcapitulo1)

        capitulo2 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=66.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo2 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo2)
        item4 = Item.objects.create(descripcion='item descripcion 1', puntos=10, subcapitulo=subcapitulo2)
        item5 = Item.objects.create(descripcion='item descripcion 2', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 3', puntos=30, subcapitulo=subcapitulo2)

        RecertificacionItemDocumento.objects.create(medico=medico1, item=item1, documento='doc1.pdf', tituloDescripcion='tituloDescripcion 1', fechaEmision='2021-04-06', puntosOtorgados=3.0,
                                                    estatus=1, observaciones='observaciones 1', notasRechazo='notasRechazo 1', razonRechazo='razonRechazo 1')
        RecertificacionItemDocumento.objects.create(medico=medico1, item=item2, documento='doc2.pdf', tituloDescripcion='tituloDescripcion 2', fechaEmision='2022-04-06', puntosOtorgados=6.0,
                                                    estatus=1, observaciones='observaciones 2', notasRechazo='notasRechazo 2', razonRechazo='razonRechazo 2')
        RecertificacionItemDocumento.objects.create(medico=medico1, item=item3, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=9.0,
                                                    estatus=1, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')

        RecertificacionItemDocumento.objects.create(medico=medico1, item=item4, documento='doc4.pdf', tituloDescripcion='tituloDescripcion 4', fechaEmision='2023-04-06', puntosOtorgados=9.0,
                                                    estatus=1, observaciones='observaciones 4', notasRechazo='notasRechazo 4', razonRechazo='razonRechazo 4')
        RecertificacionItemDocumento.objects.create(medico=medico1, item=item5, documento='doc5.pdf', tituloDescripcion='tituloDescripcion 5', fechaEmision='2023-04-06', puntosOtorgados=9.0,
                                                    estatus=1, observaciones='observaciones 5', notasRechazo='notasRechazo 5', razonRechazo='razonRechazo 5')
        RecertificacionItemDocumento.objects.create(medico=medico1, item=item6, documento='doc6.pdf', tituloDescripcion='tituloDescripcion 6', fechaEmision='2023-04-06', puntosOtorgados=9.0,
                                                    estatus=2, observaciones='observaciones 6', notasRechazo='notasRechazo 6', razonRechazo='razonRechazo 6')

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/porcentaje/medico/1/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/porcentaje/medico/11/')
        print(f'response JSON ===>>> medico no encontrado \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        RecertificacionItemDocumento.objects.filter(medico=1).delete()
        response = self.client.get('/api/recertificacion/porcentaje/medico/1/')
        print(f'response JSON ===>>> no hay documentos \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # datosMedico = Medico.objects.get(id=1)
        # print(f'--->>>datosMedicos: {datosMedico.nombre} - {datosMedico.numRegistro}')

        # querysetPAR = Capitulo.objects.aggregate(Sum('puntos'))
        # puntosAReunir = querysetPAR['puntos__sum']
        # print(f'--->>>puntosAReunir: {puntosAReunir}')

        # querysetPO = RecertificacionItemDocumento.objects.filter(medico=1, estatus=1).aggregate(Sum('puntosOtorgados'))
        # puntosObtenidos = querysetPO['puntosOtorgados__sum']
        # print(f'--->>>puntosObtenidos: {puntosObtenidos}')

        # porcentaje = round(puntosObtenidos * 100 / puntosAReunir, 2)
        # print(f'--->>>avance: {porcentaje}')


class GetPuntosPorCapituloMedico200Test(APITestCase):
    def setUp(self):
        medico1 = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=369)

        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)
        item2 = Item.objects.create(descripcion='item descripcion 2', puntos=6, subcapitulo=subcapitulo1)
        item3 = Item.objects.create(descripcion='item descripcion 3', puntos=9, subcapitulo=subcapitulo1)

        capitulo2 = Capitulo.objects.create(titulo='titulo 2', descripcion='capitulo descripcion 2', puntos=66.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo2 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo2)
        item4 = Item.objects.create(descripcion='item descripcion 1', puntos=10, subcapitulo=subcapitulo2)
        item5 = Item.objects.create(descripcion='item descripcion 2', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 3', puntos=30, subcapitulo=subcapitulo2)

        RecertificacionItemDocumento.objects.create(medico=medico1, item=item1, documento='doc1.pdf', tituloDescripcion='tituloDescripcion 1', fechaEmision='2021-04-06', puntosOtorgados=3.0,
                                                    estatus=1, observaciones='observaciones 1', notasRechazo='notasRechazo 1', razonRechazo='razonRechazo 1')
        RecertificacionItemDocumento.objects.create(medico=medico1, item=item2, documento='doc2.pdf', tituloDescripcion='tituloDescripcion 2', fechaEmision='2022-04-06', puntosOtorgados=6.0,
                                                    estatus=1, observaciones='observaciones 2', notasRechazo='notasRechazo 2', razonRechazo='razonRechazo 2')
        RecertificacionItemDocumento.objects.create(medico=medico1, item=item3, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=9.0,
                                                    estatus=1, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')

        RecertificacionItemDocumento.objects.create(medico=medico1, item=item4, documento='doc4.pdf', tituloDescripcion='tituloDescripcion 4', fechaEmision='2023-04-06', puntosOtorgados=9.0,
                                                    estatus=1, observaciones='observaciones 4', notasRechazo='notasRechazo 4', razonRechazo='razonRechazo 4')
        RecertificacionItemDocumento.objects.create(medico=medico1, item=item5, documento='doc5.pdf', tituloDescripcion='tituloDescripcion 5', fechaEmision='2023-04-06', puntosOtorgados=9.0,
                                                    estatus=1, observaciones='observaciones 5', notasRechazo='notasRechazo 5', razonRechazo='razonRechazo 5')
        RecertificacionItemDocumento.objects.create(medico=medico1, item=item6, documento='doc6.pdf', tituloDescripcion='tituloDescripcion 6', fechaEmision='2023-04-06', puntosOtorgados=9.0,
                                                    estatus=1, observaciones='observaciones 6', notasRechazo='notasRechazo 6', razonRechazo='razonRechazo 6')

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/puntos/capitulo/1/medico/1/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/puntos/capitulo/2/medico/1/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/puntos/capitulo/22/medico/1/')
        print(f'response JSON ===>>> capitulo no encontrado \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get('/api/recertificacion/puntos/capitulo/2/medico/11/')
        print(f'response JSON ===>>> medico no encontrado \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        RecertificacionItemDocumento.objects.filter(id=1).update(puntosOtorgados=100)
        response = self.client.get('/api/recertificacion/puntos/capitulo/1/medico/1/')
        print(f'response JSON ===>>> esta excedido \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # queryset = Capitulo.objects.get(id=1)
        # print(f'--->>>puntos: {queryset.puntos}')

        # querysetPO = RecertificacionItemDocumento.objects.filter(medico=1, item__subcapitulo__capitulo=1, estatus=1).aggregate(Sum('puntosOtorgados'))
        # reunidos = querysetPO['puntosOtorgados__sum']
        # print(f'--->>>reunidos: {reunidos}')

        # faltantes = round(queryset.puntos - reunidos,2)
        # print(f'--->>>faltantes: {faltantes}')

        # reunidos = reunidos + 100
        # isExcedido = True if reunidos > queryset.puntos else False
        # print(f'--->>>isExcedido: {isExcedido}')


class GetDetallesCapitulo200Test(APITestCase):
    def setUp(self):
        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)
        item2 = Item.objects.create(descripcion='item descripcion 2', puntos=6, subcapitulo=subcapitulo1)
        item3 = Item.objects.create(descripcion='item descripcion 3', puntos=9, subcapitulo=subcapitulo1)

        capitulo2 = Capitulo.objects.create(titulo='titulo 2', descripcion='capitulo descripcion 2', puntos=66.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo2 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo2)
        subcapitulo4 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 4', comentarios='subcapitulo comentarios 4', capitulo=capitulo2)
        item4 = Item.objects.create(descripcion='item descripcion 1', puntos=10, subcapitulo=subcapitulo2)
        item5 = Item.objects.create(descripcion='item descripcion 2', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 3', puntos=30, subcapitulo=subcapitulo2)

        item7 = Item.objects.create(descripcion='item descripcion 4', puntos=30, subcapitulo=subcapitulo4)
        item8 = Item.objects.create(descripcion='item descripcion 5', puntos=30, subcapitulo=subcapitulo4)
        item9 = Item.objects.create(descripcion='item descripcion 6', puntos=30, subcapitulo=subcapitulo4)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/capitulo/1/detail/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/capitulo/2/detail/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/capitulo/3/detail/')
        print(f'response JSON ===>>> no encontrado \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetItemDocumentosList200Test(APITestCase):
    def setUp(self):
        medico1 = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=369)

        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)
        item2 = Item.objects.create(descripcion='item descripcion 2', puntos=6, subcapitulo=subcapitulo1)
        item3 = Item.objects.create(descripcion='item descripcion 3', puntos=9, subcapitulo=subcapitulo1)

        capitulo2 = Capitulo.objects.create(titulo='titulo 2', descripcion='capitulo descripcion 2', puntos=66.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo2 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo2)
        subcapitulo4 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 4', comentarios='subcapitulo comentarios 4', capitulo=capitulo2)
        item4 = Item.objects.create(descripcion='item descripcion 1', puntos=10, subcapitulo=subcapitulo2)
        item5 = Item.objects.create(descripcion='item descripcion 2', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 3', puntos=30, subcapitulo=subcapitulo2)

        item7 = Item.objects.create(descripcion='item descripcion 4', puntos=30, subcapitulo=subcapitulo4)
        item8 = Item.objects.create(descripcion='item descripcion 5', puntos=30, subcapitulo=subcapitulo4)
        item9 = Item.objects.create(descripcion='item descripcion 6', puntos=30, subcapitulo=subcapitulo4)

        RecertificacionItemDocumento.objects.create(medico=medico1, item=item3, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=1, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')
        RecertificacionItemDocumento.objects.create(medico=medico1, item=item3, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=2, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')
        RecertificacionItemDocumento.objects.create(medico=medico1, item=item3, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=3, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/item/3/documentos/list/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/item/33/documentos/list/')
        print(f'response JSON ===>>> no encontrado \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostItemDocumentosCreate201Test(APITestCase):
    def setUp(self):
        medico1 = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=369)

        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)
        item2 = Item.objects.create(descripcion='item descripcion 2', puntos=6, subcapitulo=subcapitulo1)
        item3 = Item.objects.create(descripcion='item descripcion 3', puntos=9, subcapitulo=subcapitulo1)

        capitulo2 = Capitulo.objects.create(titulo='titulo 2', descripcion='capitulo descripcion 2', puntos=66.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo2 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo2)
        subcapitulo4 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 4', comentarios='subcapitulo comentarios 4', capitulo=capitulo2)
        item4 = Item.objects.create(descripcion='item descripcion 1', puntos=10, subcapitulo=subcapitulo2)
        item5 = Item.objects.create(descripcion='item descripcion 2', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 3', puntos=30, subcapitulo=subcapitulo2)

        item7 = Item.objects.create(descripcion='item descripcion 4', puntos=30, subcapitulo=subcapitulo4)
        item8 = Item.objects.create(descripcion='item descripcion 5', puntos=30, subcapitulo=subcapitulo4)
        item9 = Item.objects.create(descripcion='item descripcion 6', puntos=30, subcapitulo=subcapitulo4)

        archivo = open('./uploads/image_4.png', 'rb')
        documento = SimpleUploadedFile(archivo.name, archivo.read(), content_type='image/png')

        self.json = {
            "documento": documento,
            "tituloDescripcion": "tituloDescripcion 3",
            "fechaEmision": "2023-04-06",
            # "puntosOtorgados": "3.00",
            # "estatus": 3,
            # "observaciones": "observaciones 3",
            # "notasRechazo": "notasRechazo 3",
            # "razonRechazo": "razonRechazo 3",
            "medico": 1,
            "item": 3
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        cuenta = RecertificacionItemDocumento.objects.count()
        print(f'--->>>cuenta: {cuenta}')
        response = self.client.post('/api/recertificacion/documento/create/', data=self.json, format='multipart')
        print(f'response JSON ===>>> OK \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cuenta = RecertificacionItemDocumento.objects.count()
        print(f'--->>>cuenta: {cuenta}')


class GetCertificadosMedicoList200Test(APITestCase):
    def setUp(self):
        medico1 = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=369)
        medico2 = Medico.objects.create(
            id=2, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=369)

        Certificado.objects.create(medico=medico1, documento='certificado_de_chingon1.PDF', descripcion='es un chingon el tipo1', isVencido=False, fechaCertificacion='2021-04-06',
                                   fechaCaducidad='2026-04-06', estatus=1)
        Certificado.objects.create(medico=medico2, documento='certificado_de_chingon2.PDF', descripcion='es un chingon el tipo2', isVencido=True, fechaCertificacion='2000-05-06',
                                   fechaCaducidad='2005-05-06', estatus=3)
        Certificado.objects.create(medico=medico1, documento='certificado_de_chingon3.PDF', descripcion='es un chingon el tipo3', isVencido=True, fechaCertificacion='2016-06-06',
                                   fechaCaducidad='2021-06-06', estatus=2)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/medico/1/certificados/list/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/medico/2/certificados/list/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/medico/3/certificados/list/')
        print(f'response JSON ===>>> no hay \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetItemDocumentosFilteredList200Test(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)
        item2 = Item.objects.create(descripcion='item descripcion 2', puntos=6, subcapitulo=subcapitulo1)
        item3 = Item.objects.create(descripcion='item descripcion 3', puntos=9, subcapitulo=subcapitulo1)

        capitulo2 = Capitulo.objects.create(titulo='titulo 2', descripcion='capitulo descripcion 2', puntos=66.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo2 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo2)
        subcapitulo4 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 4', comentarios='subcapitulo comentarios 4', capitulo=capitulo2)
        item4 = Item.objects.create(descripcion='item descripcion 1', puntos=10, subcapitulo=subcapitulo2)
        item5 = Item.objects.create(descripcion='item descripcion 2', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 3', puntos=30, subcapitulo=subcapitulo2)

        item7 = Item.objects.create(descripcion='item descripcion 4', puntos=30, subcapitulo=subcapitulo4)
        item8 = Item.objects.create(descripcion='item descripcion 5', puntos=30, subcapitulo=subcapitulo4)
        item9 = Item.objects.create(descripcion='item descripcion 6', puntos=30, subcapitulo=subcapitulo4)

        RecertificacionItemDocumento.objects.create(medico=medico3, item=item3, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=1, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')
        RecertificacionItemDocumento.objects.create(medico=medico6, item=item6, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=2, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')
        RecertificacionItemDocumento.objects.create(medico=medico9, item=item9, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=3, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')

        Certificado.objects.create(medico=medico3, documento='certificado_de_chingon1.PDF', descripcion='es un chingon el tipo1', isVencido=False, fechaCertificacion='2021-04-06',
                                   fechaCaducidad='2026-04-06', estatus=1)
        Certificado.objects.create(medico=medico6, documento='certificado_de_chingon2.PDF', descripcion='es un chingon el tipo2', isVencido=False, fechaCertificacion='2000-05-06',
                                   fechaCaducidad='2005-05-06', estatus=3)
        Certificado.objects.create(medico=medico9, documento='certificado_de_chingon3.PDF', descripcion='es un chingon el tipo3', isVencido=False, fechaCertificacion='2016-06-06',
                                   fechaCaducidad='2021-06-06', estatus=2)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # response = self.client.get('/api/recertificacion/documento/all/all/0/list/') # regresa TODOS
        # print(f'response JSON ===>>> N:all - A:all - E:0 \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Medico.objects.filter(id=3).update(nombre='gabriel')
        # response = self.client.get('/api/recertificacion/documento/gabriel/all/0/list/') # regresa gabriel quiroz y gabriel tolentino
        # print(f'response JSON ===>>> N:gabriel - A:all - E:0 \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        Medico.objects.filter(id=3).update(nombre='laura', apPaterno='olvéra')
        Medico.objects.filter(id=9).update(apPaterno='olvéra')
        response = self.client.get('/api/recertificacion/documento/all/Olvéra/0/list/')  # regresa laura olvera y gabriel olvera
        print(f'response JSON ===>>> N:all - A:olvera - E:0 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/recertificacion/documento/laura/all/2/list/') # regresa laura cabrera
        # print(f'response JSON ===>>> N:laura - A:all - E:2 \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/recertificacion/documento/all/all/3/list/')  # regresa el que esta Pendiente
        # print(f'response JSON ===>>> N:all - A:all - E:3 \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetItemDocumentosDetail200Test(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)
        item2 = Item.objects.create(descripcion='item descripcion 2', puntos=6, subcapitulo=subcapitulo1)
        item3 = Item.objects.create(descripcion='item descripcion 3', puntos=9, subcapitulo=subcapitulo1)

        capitulo2 = Capitulo.objects.create(titulo='titulo 2', descripcion='capitulo descripcion 2', puntos=66.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo2 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo2)
        subcapitulo4 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 4', comentarios='subcapitulo comentarios 4', capitulo=capitulo2)
        item4 = Item.objects.create(descripcion='item descripcion 1', puntos=10, subcapitulo=subcapitulo2)
        item5 = Item.objects.create(descripcion='item descripcion 2', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 3', puntos=30, subcapitulo=subcapitulo2)

        item7 = Item.objects.create(descripcion='item descripcion 4', puntos=30, subcapitulo=subcapitulo4)
        item8 = Item.objects.create(descripcion='item descripcion 5', puntos=30, subcapitulo=subcapitulo4)
        item9 = Item.objects.create(descripcion='item descripcion 6', puntos=30, subcapitulo=subcapitulo4)

        RecertificacionItemDocumento.objects.create(medico=medico3, item=item3, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=1, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')
        RecertificacionItemDocumento.objects.create(medico=medico6, item=item6, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=2, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')
        RecertificacionItemDocumento.objects.create(medico=medico9, item=item9, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=3, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')

        Certificado.objects.create(medico=medico3, documento='certificado_de_chingon1.PDF', descripcion='es un chingon el tipo1', isVencido=False, fechaCertificacion='2021-04-06',
                                   fechaCaducidad='2026-04-06', estatus=1)
        Certificado.objects.create(medico=medico6, documento='certificado_de_chingon2.PDF', descripcion='es un chingon el tipo2', isVencido=False, fechaCertificacion='2000-05-06',
                                   fechaCaducidad='2005-05-06', estatus=3)
        Certificado.objects.create(medico=medico9, documento='certificado_de_chingon3.PDF', descripcion='es un chingon el tipo3', isVencido=False, fechaCertificacion='2016-06-06',
                                   fechaCaducidad='2021-06-06', estatus=2)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/documento/1/detail/')  # regresa TODOS
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutItemDocumentosAceptar200Test(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)
        item2 = Item.objects.create(descripcion='item descripcion 2', puntos=6, subcapitulo=subcapitulo1)
        item3 = Item.objects.create(descripcion='item descripcion 3', puntos=9, subcapitulo=subcapitulo1)

        capitulo2 = Capitulo.objects.create(titulo='titulo 2', descripcion='capitulo descripcion 2', puntos=66.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo2 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo2)
        subcapitulo4 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 4', comentarios='subcapitulo comentarios 4', capitulo=capitulo2)
        item4 = Item.objects.create(descripcion='item descripcion 1', puntos=10, subcapitulo=subcapitulo2)
        item5 = Item.objects.create(descripcion='item descripcion 2', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 3', puntos=30, subcapitulo=subcapitulo2)

        item7 = Item.objects.create(descripcion='item descripcion 4', puntos=30, subcapitulo=subcapitulo4)
        item8 = Item.objects.create(descripcion='item descripcion 5', puntos=30, subcapitulo=subcapitulo4)
        item9 = Item.objects.create(descripcion='item descripcion 6', puntos=30, subcapitulo=subcapitulo4)

        RecertificacionItemDocumento.objects.create(medico=medico3, item=item3, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=1, observaciones='observaciones 1', notasRechazo='notasRechazo 1', razonRechazo='razonRechazo 1')
        RecertificacionItemDocumento.objects.create(medico=medico6, item=item6, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=2, observaciones='observaciones 2', notasRechazo='notasRechazo 2', razonRechazo='razonRechazo 2')
        RecertificacionItemDocumento.objects.create(medico=medico9, item=item9, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=3, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')

        Certificado.objects.create(medico=medico3, documento='certificado_de_chingon1.PDF', descripcion='es un chingon el tipo1', isVencido=False, fechaCertificacion='2021-04-06',
                                   fechaCaducidad='2026-04-06', estatus=1)
        Certificado.objects.create(medico=medico6, documento='certificado_de_chingon2.PDF', descripcion='es un chingon el tipo2', isVencido=False, fechaCertificacion='2000-05-06',
                                   fechaCaducidad='2005-05-06', estatus=3)
        Certificado.objects.create(medico=medico9, documento='certificado_de_chingon3.PDF', descripcion='es un chingon el tipo3', isVencido=False, fechaCertificacion='2016-06-06',
                                   fechaCaducidad='2021-06-06', estatus=2)

        self.json = {
            "puntosOtorgados": 99.9
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put('/api/recertificacion/documento/aceptar/1/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        # print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put('/api/recertificacion/documento/aceptar/11/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> no encontrado 404 \n {json.dumps(response.json())} \n ---')
        # print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.json = {
            "puntosOtorgados": "x99.9"
        }
        response = self.client.put('/api/recertificacion/documento/aceptar/1/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> bad request 400 \n {json.dumps(response.json())} \n ---')
        # print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PutItemDocumentosRechazar200Test(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)
        item2 = Item.objects.create(descripcion='item descripcion 2', puntos=6, subcapitulo=subcapitulo1)
        item3 = Item.objects.create(descripcion='item descripcion 3', puntos=9, subcapitulo=subcapitulo1)

        capitulo2 = Capitulo.objects.create(titulo='titulo 2', descripcion='capitulo descripcion 2', puntos=66.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo2 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo2)
        subcapitulo4 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 4', comentarios='subcapitulo comentarios 4', capitulo=capitulo2)
        item4 = Item.objects.create(descripcion='item descripcion 1', puntos=10, subcapitulo=subcapitulo2)
        item5 = Item.objects.create(descripcion='item descripcion 2', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 3', puntos=30, subcapitulo=subcapitulo2)

        item7 = Item.objects.create(descripcion='item descripcion 4', puntos=30, subcapitulo=subcapitulo4)
        item8 = Item.objects.create(descripcion='item descripcion 5', puntos=30, subcapitulo=subcapitulo4)
        item9 = Item.objects.create(descripcion='item descripcion 6', puntos=30, subcapitulo=subcapitulo4)

        RecertificacionItemDocumento.objects.create(medico=medico3, item=item3, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=1, observaciones='observaciones 1', notasRechazo='notasRechazo 1', razonRechazo='razonRechazo 1')
        RecertificacionItemDocumento.objects.create(medico=medico6, item=item6, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=2, observaciones='observaciones 2', notasRechazo='notasRechazo 2', razonRechazo='razonRechazo 2')
        RecertificacionItemDocumento.objects.create(medico=medico9, item=item9, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=3, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')

        Certificado.objects.create(medico=medico3, documento='certificado_de_chingon1.PDF', descripcion='es un chingon el tipo1', isVencido=False, fechaCertificacion='2021-04-06',
                                   fechaCaducidad='2026-04-06', estatus=1)
        Certificado.objects.create(medico=medico6, documento='certificado_de_chingon2.PDF', descripcion='es un chingon el tipo2', isVencido=False, fechaCertificacion='2000-05-06',
                                   fechaCaducidad='2005-05-06', estatus=3)
        Certificado.objects.create(medico=medico9, documento='certificado_de_chingon3.PDF', descripcion='es un chingon el tipo3', isVencido=False, fechaCertificacion='2016-06-06',
                                   fechaCaducidad='2021-06-06', estatus=2)

        self.json = {
            "puntosOtorgados": 99.9,
            "notasRechazo": "notas de rechazo INPUT",
            "razonRechazo": "razon de rechazo INPUT",
            "observaciones": "observaciones INPUT"
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put('/api/recertificacion/documento/rechazar/1/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        # print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put('/api/recertificacion/documento/rechazar/11/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> no encontrado 404 \n {json.dumps(response.json())} \n ---')
        # print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # no hay bad request porque le pone el valor de 0 en automatico


class PutItemDocumentosReasignar200Test(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)
        item2 = Item.objects.create(descripcion='item descripcion 2', puntos=6, subcapitulo=subcapitulo1)
        item3 = Item.objects.create(descripcion='item descripcion 3', puntos=9, subcapitulo=subcapitulo1)

        capitulo2 = Capitulo.objects.create(titulo='titulo 2', descripcion='capitulo descripcion 2', puntos=66.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo2 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo2)
        subcapitulo4 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 4', comentarios='subcapitulo comentarios 4', capitulo=capitulo2)
        item4 = Item.objects.create(descripcion='item descripcion 1', puntos=10, subcapitulo=subcapitulo2)
        item5 = Item.objects.create(descripcion='item descripcion 2', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 3', puntos=30, subcapitulo=subcapitulo2)

        item7 = Item.objects.create(descripcion='item descripcion 4', puntos=30, subcapitulo=subcapitulo4)
        item8 = Item.objects.create(descripcion='item descripcion 5', puntos=30, subcapitulo=subcapitulo4)
        item9 = Item.objects.create(descripcion='item descripcion 6', puntos=30, subcapitulo=subcapitulo4)

        RecertificacionItemDocumento.objects.create(medico=medico3, item=item3, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=3, observaciones='observaciones 1', notasRechazo='notasRechazo 1', razonRechazo='razonRechazo 1')
        RecertificacionItemDocumento.objects.create(medico=medico6, item=item6, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=3, observaciones='observaciones 2', notasRechazo='notasRechazo 2', razonRechazo='razonRechazo 2')
        RecertificacionItemDocumento.objects.create(medico=medico9, item=item9, documento='doc3.pdf', tituloDescripcion='tituloDescripcion 3', fechaEmision='2023-04-06', puntosOtorgados=3.0,
                                                    estatus=3, observaciones='observaciones 3', notasRechazo='notasRechazo 3', razonRechazo='razonRechazo 3')

        Certificado.objects.create(medico=medico3, documento='certificado_de_chingon1.PDF', descripcion='es un chingon el tipo1', isVencido=False, fechaCertificacion='2021-04-06',
                                   fechaCaducidad='2026-04-06', estatus=1)
        Certificado.objects.create(medico=medico6, documento='certificado_de_chingon2.PDF', descripcion='es un chingon el tipo2', isVencido=False, fechaCertificacion='2000-05-06',
                                   fechaCaducidad='2005-05-06', estatus=3)
        Certificado.objects.create(medico=medico9, documento='certificado_de_chingon3.PDF', descripcion='es un chingon el tipo3', isVencido=False, fechaCertificacion='2016-06-06',
                                   fechaCaducidad='2021-06-06', estatus=2)

        self.json = {
            "puntosOtorgados": 99.9,
            "item": 8,
            "observaciones": "se reasigno"
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/documento/1/detail/')  # regresa TODOS
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put('/api/recertificacion/documento/reasignar/1/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        # print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/documento/1/detail/')  # regresa TODOS
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put('/api/recertificacion/documento/reasignar/11/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> no encontrado 404 \n {json.dumps(response.json())} \n ---')
        # print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # no hay bad request porque le pone el valor de 0 en automatico


class GetSeveralSelectList200Test(APITestCase):
    def setUp(self):
        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)
        item2 = Item.objects.create(descripcion='item descripcion 2', puntos=6, subcapitulo=subcapitulo1)
        item3 = Item.objects.create(descripcion='item descripcion 3', puntos=9, subcapitulo=subcapitulo1)

        capitulo2 = Capitulo.objects.create(titulo='titulo 2', descripcion='capitulo descripcion 2', puntos=66.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo2 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo2)
        subcapitulo4 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 4', comentarios='subcapitulo comentarios 4', capitulo=capitulo2)
        item4 = Item.objects.create(descripcion='item descripcion 4', puntos=10, subcapitulo=subcapitulo2)
        item5 = Item.objects.create(descripcion='item descripcion 5', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 6', puntos=30, subcapitulo=subcapitulo2)

        item7 = Item.objects.create(descripcion='item descripcion 7', puntos=30, subcapitulo=subcapitulo4)
        item8 = Item.objects.create(descripcion='item descripcion 8', puntos=30, subcapitulo=subcapitulo4)
        item9 = Item.objects.create(descripcion='item descripcion 9', puntos=30, subcapitulo=subcapitulo4)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # capitulos
        response = self.client.get('/api/recertificacion/capitulo/list/')
        print(f'response JSON ===>>> capitulos OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # subcapitulos
        response = self.client.get('/api/recertificacion/subcapitulo/2/list/')
        print(f'response JSON ===>>> subcapitulos OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/subcapitulo/3/list/')
        print(f'response JSON ===>>> subcapitulos no existe \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # items
        response = self.client.get('/api/recertificacion/item/2/list/')
        print(f'response JSON ===>>> items OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/item/33/list/')
        print(f'response JSON ===>>> items no existe \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PutActualizaVigenciaCertificados200Test(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        Certificado.objects.create(medico=medico9, documento='certificado_de_chingon3.PDF', descripcion='vigente(1) false', isVencido=False, fechaCertificacion='2016-06-06',
                                   fechaCaducidad=date.today()+relativedelta(years=3), estatus=1)
        Certificado.objects.create(medico=medico3, documento='certificado_de_chingon3.PDF', descripcion='vencido(3) true', isVencido=False, fechaCertificacion='2016-06-06',
                                   fechaCaducidad=date.today()-relativedelta(days=66), estatus=1)
        Certificado.objects.create(medico=medico6, documento='certificado_de_chingon2.PDF', descripcion='por vencer(2) false', isVencido=False, fechaCertificacion='2000-05-06',
                                   fechaCaducidad=date.today()+relativedelta(days=364), estatus=1)
        Certificado.objects.create(medico=medico3, documento='certificado_de_chingon1.PDF', descripcion='vencido(3) true', isVencido=False, fechaCertificacion='2021-04-06',
                                   fechaCaducidad=date.today()-relativedelta(months=9), estatus=1)
        Certificado.objects.create(medico=medico9, documento='certificado_de_chingon3.PDF', descripcion='vigente(1) false', isVencido=False, fechaCertificacion='2016-06-06',
                                   fechaCaducidad=date.today()+relativedelta(years=1, months=3), estatus=1)
        Certificado.objects.create(medico=medico6, documento='certificado_de_chingon3.PDF', descripcion='por vencer(2) false', isVencido=False, fechaCertificacion='2016-06-06',
                                   fechaCaducidad=date.today()+relativedelta(days=159), estatus=1)
        Certificado.objects.create(medico=medico6, documento='certificado_de_chingon3.PDF', descripcion='vencido(3) true', isVencido=False, fechaCertificacion='2016-06-06',
                                   fechaCaducidad=date.today()-relativedelta(months=11), estatus=1)
        Certificado.objects.create(medico=medico6, documento='certificado_de_chingon3.PDF', descripcion='vencido(3) true', isVencido=False, fechaCertificacion='2016-06-06',
                                   fechaCaducidad=date.today()-relativedelta(days=1), estatus=1)
        Certificado.objects.create(medico=medico6, documento='certificado_de_chingon3.PDF', descripcion='por vencer(2) false', isVencido=False, fechaCertificacion='2016-06-06',
                                   fechaCaducidad=date.today()+relativedelta(days=99), estatus=1)
        Certificado.objects.create(medico=medico6, documento='certificado_de_chingon3.PDF', descripcion='vigente(1) false', isVencido=False, fechaCertificacion='2016-06-06',
                                   fechaCaducidad=date.today()+relativedelta(years=1, days=9), estatus=1)

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put('/api/recertificacion/actualiza-vigencia-certificados/update/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        # print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        queryset = Certificado.objects.all().values_list('id', 'fechaCaducidad', 'estatus', 'isVencido', 'descripcion').order_by('id')
        for dato in queryset:
            print(f'--->>>dato: {dato[0]} - {dato[1]} - {dato[2]} - {dato[3]} - {dato[4]}')


class PostSolicitarExamen201Test(APITestCase):
    def setUp(self):
        self.medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        FechasExamenRecertificacion.objects.create(fechaExamen='2021-04-01', descripcion='primer fecha')
        FechasExamenRecertificacion.objects.create(fechaExamen='2021-08-01', descripcion='segunda fecha')
        FechasExamenRecertificacion.objects.create(fechaExamen='2021-12-01', descripcion='tercer fecha')

        self.json = {
            "medico": 9,
        }

        self.user = User.objects.create_user(username='gabriel')  # , is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # cuenta = PorExamen.objects.count()
        # print(f'--->>>cuenta: {cuenta}')

        # response = self.client.post('/api/recertificacion/solicitud-examen/create/', data=json.dumps(self.json), content_type="application/json")
        # print(f'response JSON ===>>> OK \n {json.dumps(response.data, ensure_ascii=False)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # # PorExamen.objects.create(medico=self.medico9, estatus=3, isAprobado=False, calificacion=0) #ya esxiste del anterior
        # response = self.client.post('/api/recertificacion/solicitud-examen/create/', data=json.dumps(self.json), content_type="application/json")
        # print(f'response JSON ===>>> ya se genero una solicitud de examen \n {json.dumps(response.data, ensure_ascii=False)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # self.json = {
        #     "medico": 4,
        # }
        # response = self.client.post('/api/recertificacion/solicitud-examen/create/', data=json.dumps(self.json), content_type="application/json")
        # print(f'response JSON ===>>> no existe medico \n {json.dumps(response.data, ensure_ascii=False)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # cuenta = PorExamen.objects.count()
        # print(f'--->>>cuenta: {cuenta}')

        FechasExamenRecertificacion.objects.filter(id=2).delete()
        FechasExamenRecertificacion.objects.filter(id=3).delete()
        response = self.client.post('/api/recertificacion/solicitud-examen/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> OK \n {json.dumps(response.data, ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostDocumento201Test(APITestCase):
    def setUp(self):
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

        catTiposDocumento1 = CatTiposDocumento.objects.create(descripcion='Revalidación')
        catTiposDocumento2 = CatTiposDocumento.objects.create(descripcion='CURP')
        catTiposDocumento3 = CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        catTiposDocumento4 = CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        catTiposDocumento5 = CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        catTiposDocumento6 = CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        catTiposDocumento7 = CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        catTiposDocumento8 = CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        catTiposDocumento9 = CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        catTiposDocumento10 = CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')
        catTiposDocumento11 = CatTiposDocumento.objects.create(descripcion='Ficha de Registro')
        catTiposDocumento12 = CatTiposDocumento.objects.create(descripcion='Fotografía Digital')
        catTiposDocumento13 = CatTiposDocumento.objects.create(descripcion='Certificado')
        catTiposDocumento14 = CatTiposDocumento.objects.create(descripcion='Fotografía Diploma')

        self.medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        porExamen = PorExamen.objects.create(medico=self.medico9, estatus=3, isAprobado=False, calificacion=0)

        PorExamenDocumento.objects.create(porExamen=porExamen, catTiposDocumento=catTiposDocumento13, documento='documento6', isAceptado=True)
        PorExamenDocumento.objects.create(porExamen=porExamen, catTiposDocumento=catTiposDocumento6, documento='documento6', isAceptado=True)
        PorExamenDocumento.objects.create(porExamen=porExamen, catTiposDocumento=catTiposDocumento12, documento='documento6', isAceptado=True)
        PorExamenDocumento.objects.create(porExamen=porExamen, catTiposDocumento=catTiposDocumento14, documento='documento6', isAceptado=True)
        PorExamenDocumento.objects.create(porExamen=porExamen, catTiposDocumento=catTiposDocumento4, documento='documento6', isAceptado=True)

        archivo = open('./uploads/testUnit.png', 'rb')
        documento = SimpleUploadedFile(archivo.name, archivo.read(), content_type='image/png')

        self.json = {
            "documento": documento,
            "porExamen": 1,
            # "catTiposDocumento": 6,
            # "isAceptado": True,
        }

        archivoO = open('./uploads/testUnit.png', 'rb')
        documentoO = SimpleUploadedFile(archivoO.name, archivoO.read(), content_type='image/png')

        self.jsonO = {
            "documento": documentoO,
            "porExamen": 1,
            # "catTiposDocumento": 6,
            # "isAceptado": True,
        }

        archivoError = open('./uploads/testUnit.png', 'rb')
        documentoError = SimpleUploadedFile(archivoError.name, archivoError.read(), content_type='image/png')

        self.jsonError = {
            "documento": documentoError,
            "porExamen": 111,
            # "catTiposDocumento": 6,
            # "isAceptado": True,
        }

        self.user = User.objects.create_user(username='gabriel')  # , is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # response = self.client.post('/api/recertificacion/documento/cedula-especialidad/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> OK \n {json.dumps(response.data, ensure_ascii=False)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # response = self.client.post('/api/recertificacion/documento/certificado/create/', data=self.jsonO, format='multipart')
        # print(f'response JSON ===>>> OK \n {json.dumps(response.data, ensure_ascii=False)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/api/recertificacion/documento/carta-solicitud/create/', data=self.jsonO, format='multipart')
        print(f'response JSON ===>>> OK \n {json.dumps(response.data, ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # response = self.client.post('/api/recertificacion/documento/foto/create/', data=self.jsonO, format='multipart')
        # print(f'response JSON ===>>> OK \n {json.dumps(response.data, ensure_ascii=False)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/api/recertificacion/documento/certificado/create/', data=self.jsonError, format='multipart')
        print(f'response JSON ===>>> OK \n {json.dumps(response.data, ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        cuenta = Notificacion.objects.count()
        if cuenta != 0:
            dato = Notificacion.objects.get(id=1)
            print(f'--->>>dato: titulo: {dato.titulo}, mensaje: {dato.mensaje}, destinatario: {dato.destinatario}, remitente: {dato.remitente}')


class GetCostoAPagar200Test(APITestCase):
    def setUp(self):
        CatPagos.objects.create(descripcion='ECV - Examen loco!!!', precio=369.69, tipo=1)
        CatPagos.objects.create(descripcion='RC - Examen crazy!!!', precio=963.69, tipo=6)

        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        PorExamen.objects.create(id=6, medico=medico9, estatus=3, isAprobado=False, calificacion=0, isPagado=False, isAceptado=True)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # Si puede pagar
        response = self.client.get('/api/recertificacion/medico/9/a-pagar/examen/')
        print(f'response JSON ===>>> OK - examen \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/medico/9/a-pagar/renovacion/')
        print(f'response JSON ===>>> OK - renovacion \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/medico/3/a-pagar/renovacion/')
        print(f'response JSON ===>>> 404 no existe medico - renovacion \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get('/api/recertificacion/medico/3/a-pagar/examen/')
        print(f'response JSON ===>>> 404 no existe medico - examen \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        PorExamen.objects.filter(id=6).update(isAceptado=False)
        response = self.client.get('/api/recertificacion/medico/9/a-pagar/examen/')
        print(f'response JSON ===>>> 409 no puede pagar - examen \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class PutExamenPagado200Test(APITestCase):
    def setUp(self):
        CatPagos.objects.create(descripcion='ECV - Examen loco!!!', precio=369.69, tipo=1)
        CatPagos.objects.create(descripcion='RC - Examen crazy!!!', precio=963.69, tipo=6)

        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        PorExamen.objects.create(id=3, medico=medico9, estatus=3, isAprobado=False, calificacion=0, isPagado=False, isAceptado=True)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = PorExamen.objects.get(id=3)
        print(f'--->>>ANTES dato: {dato.id} - {dato.isPagado}')

        response = self.client.put('/api/recertificacion/examen/3/pagado/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = PorExamen.objects.get(id=3)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.isPagado}')

        PorExamen.objects.filter(id=3).update(isAceptado=False)
        response = self.client.put('/api/recertificacion/examen/3/pagado/')
        print(f'response JSON ===>>> 409 no tiene permitido \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        response = self.client.put('/api/recertificacion/examen/1/pagado/')
        print(f'response JSON ===>>> 404 no existe \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostRenovacionPagado201Test(APITestCase):
    def setUp(self):
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        archivo = open('./uploads/testUnit.png', 'rb')
        documento = SimpleUploadedFile(archivo.name, archivo.read(), content_type='image/png')
        documentoVacio = None

        self.json = {
            # "documento": documentoVacio,
            # "descripcion": "tituloDescripcion 3",
            # "isVencido": False,
            # "estatus": 1,
            # "fechaCertificacion": "2021-04-06",
            # "fechaCaducidad": "2021-04-06",
            "medico": 9,
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/recertificacion/renovacion/pagado/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> OK \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        datos = Certificado.objects.get(id=1)
        print(f'--->datos: id:{datos.id} - fechaCertificacion:{datos.fechaCertificacion} - fechaCaducidad:{datos.fechaCaducidad}')


class GetPorExamenFilteredList200Test(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        fechaExamen1 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-04-01', descripcion='primer fecha')
        fechaExamen2 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-08-01', descripcion='segunda fecha')
        fechaExamen3 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-12-01', descripcion='tercera fecha')

        PorExamen.objects.create(medico=medico9, estatus=3, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen2)  # 1
        PorExamen.objects.create(medico=medico6, estatus=2, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 2
        PorExamen.objects.create(medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 3
        PorExamen.objects.create(medico=medico9, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 4
        PorExamen.objects.create(medico=medico9, estatus=3, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 5
        PorExamen.objects.create(medico=medico6, estatus=2, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 6
        PorExamen.objects.create(medico=medico6, estatus=2, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 7
        PorExamen.objects.create(medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 8
        PorExamen.objects.create(medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 9
        PorExamen.objects.create(medico=medico9, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 10

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/por-examen/list/?nombreNS=Gabriel')
        print(f'response JSON ===>>> nombreNS=gabriel \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/por-examen/list/?apPaternoNS=tolentinO')
        print(f'response JSON ===>>> apPaternoNS=tolentino \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        Medico.objects.all().update(apPaterno='quiroz')
        response = self.client.get('/api/recertificacion/por-examen/list/?nombreNS=laura&apPaternoNS=quiroz')
        print(f'response JSON ===>>> nombreNS=laura&apPaternoNS=quiroz \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/por-examen/list/?nombreNS=GABRIEL&estatus=3')
        print(f'response JSON ===>>> nombreNS=GABRIEL&estatus=3 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/por-examen/list/?apPaternoNS=quiroz')
        print(f'response JSON ===>>> apPaternoNS=quiroz \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/por-examen/list/?nombreNS=Gabriel&fechaExamen=1')
        print(f'response JSON ===>>> nombreNS=gabriel \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetPorExamenDocumentosList200Test(APITestCase):
    def setUp(self):
        catTiposDocumento1 = CatTiposDocumento.objects.create(descripcion='Revalidación')
        catTiposDocumento2 = CatTiposDocumento.objects.create(descripcion='CURP')
        catTiposDocumento3 = CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        catTiposDocumento4 = CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        catTiposDocumento5 = CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        catTiposDocumento6 = CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        catTiposDocumento7 = CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        catTiposDocumento8 = CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        catTiposDocumento9 = CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        catTiposDocumento10 = CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')
        catTiposDocumento11 = CatTiposDocumento.objects.create(descripcion='Ficha de Registro')
        catTiposDocumento12 = CatTiposDocumento.objects.create(descripcion='Fotografía')
        catTiposDocumento13 = CatTiposDocumento.objects.create(descripcion='Certificado')

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        porExamen9 = PorExamen.objects.create(id=9, medico=medico9, estatus=3, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        porExamen6 = PorExamen.objects.create(id=6, medico=medico6, estatus=2, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        porExamen3 = PorExamen.objects.create(id=3, medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)

        PorExamenDocumento.objects.create(porExamen=porExamen9, catTiposDocumento=catTiposDocumento9, documento='documento9', isAceptado=False)
        PorExamenDocumento.objects.create(porExamen=porExamen9, catTiposDocumento=catTiposDocumento6, documento='documento6', isAceptado=False)
        PorExamenDocumento.objects.create(porExamen=porExamen9, catTiposDocumento=catTiposDocumento3, documento='documento3', isAceptado=False)
        PorExamenDocumento.objects.create(porExamen=porExamen6, catTiposDocumento=catTiposDocumento1, documento='documento1', isAceptado=False)
        PorExamenDocumento.objects.create(porExamen=porExamen3, catTiposDocumento=catTiposDocumento2, documento='documento2', isAceptado=False)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/por-examen/9/documentos/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/por-examen/3/documentos/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/por-examen/1/documentos/list/')
        print(f'response JSON ===>>> no existe \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # cuentaPorExamen = PorExamen.objects.all().count()
        # print(f'--->cuentaPorExamen: {cuentaPorExamen}')
        # cuentaPEDocs = PorExamenDocumento.objects.filter(porExamen=9).count()
        # print(f'--->cuentaPorExamen: {cuentaPEDocs}')

        # PorExamen.objects.filter(id=9).delete()
        # cuentaPorExamen = PorExamen.objects.all().count()
        # print(f'--->cuentaPorExamen: {cuentaPorExamen}')
        # cuentaPEDocs = PorExamenDocumento.objects.filter(porExamen=9).count()
        # print(f'--->cuentaPorExamen: {cuentaPEDocs}')


class PutPorExamenDocumentoAceptar200Test(APITestCase):
    def setUp(self):
        catTiposDocumento1 = CatTiposDocumento.objects.create(descripcion='Revalidación')
        catTiposDocumento2 = CatTiposDocumento.objects.create(descripcion='CURP')
        catTiposDocumento3 = CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        catTiposDocumento4 = CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        catTiposDocumento5 = CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        catTiposDocumento6 = CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        catTiposDocumento7 = CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        catTiposDocumento8 = CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        catTiposDocumento9 = CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        catTiposDocumento10 = CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')
        catTiposDocumento11 = CatTiposDocumento.objects.create(descripcion='Ficha de Registro')
        catTiposDocumento12 = CatTiposDocumento.objects.create(descripcion='Fotografía')
        catTiposDocumento13 = CatTiposDocumento.objects.create(descripcion='Certificado')

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        porExamen9 = PorExamen.objects.create(id=9, medico=medico9, estatus=3, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        porExamen6 = PorExamen.objects.create(id=6, medico=medico6, estatus=2, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        porExamen3 = PorExamen.objects.create(id=3, medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)

        PorExamenDocumento.objects.create(porExamen=porExamen9, catTiposDocumento=catTiposDocumento9, documento='documento9', isAceptado=False)
        PorExamenDocumento.objects.create(porExamen=porExamen9, catTiposDocumento=catTiposDocumento6, documento='documento6', isAceptado=False)
        PorExamenDocumento.objects.create(porExamen=porExamen9, catTiposDocumento=catTiposDocumento3, documento='documento3', isAceptado=False)
        PorExamenDocumento.objects.create(porExamen=porExamen6, catTiposDocumento=catTiposDocumento1, documento='documento1', isAceptado=False)
        PorExamenDocumento.objects.create(porExamen=porExamen3, catTiposDocumento=catTiposDocumento2, documento='documento2', isAceptado=False)

        self.json = {
            "isAceptado": True
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        datos = PorExamenDocumento.objects.get(id=2)
        print(f'--->>>dato: {datos.id} - {datos.isAceptado}')
        response = self.client.put('/api/recertificacion/por-examen/documento/aceptar/2/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        # print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        datos = PorExamenDocumento.objects.get(id=2)
        print(f'--->>>dato: {datos.id} - {datos.isAceptado}')

        response = self.client.put('/api/recertificacion/por-examen/documento/aceptar/22/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> no encotrado 404 \n {json.dumps(response.json())} \n ---')
        # print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PutPorExamenDocumentoRechazar200Test(APITestCase):
    def setUp(self):
        catTiposDocumento1 = CatTiposDocumento.objects.create(descripcion='Revalidación')
        catTiposDocumento2 = CatTiposDocumento.objects.create(descripcion='CURP')
        catTiposDocumento3 = CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        catTiposDocumento4 = CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        catTiposDocumento5 = CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        catTiposDocumento6 = CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        catTiposDocumento7 = CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        catTiposDocumento8 = CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        catTiposDocumento9 = CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        catTiposDocumento10 = CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')
        catTiposDocumento11 = CatTiposDocumento.objects.create(descripcion='Ficha de Registro')
        catTiposDocumento12 = CatTiposDocumento.objects.create(descripcion='Fotografía')
        catTiposDocumento13 = CatTiposDocumento.objects.create(descripcion='Certificado')

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        porExamen9 = PorExamen.objects.create(id=9, medico=medico9, estatus=3, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        porExamen6 = PorExamen.objects.create(id=6, medico=medico6, estatus=2, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        porExamen3 = PorExamen.objects.create(id=3, medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)

        PorExamenDocumento.objects.create(porExamen=porExamen9, catTiposDocumento=catTiposDocumento9, documento='documento9', isAceptado=False)
        PorExamenDocumento.objects.create(porExamen=porExamen9, catTiposDocumento=catTiposDocumento6, documento='documento6', isAceptado=False)
        PorExamenDocumento.objects.create(porExamen=porExamen9, catTiposDocumento=catTiposDocumento3, documento='documento3', isAceptado=False)
        PorExamenDocumento.objects.create(porExamen=porExamen6, catTiposDocumento=catTiposDocumento1, documento='documento1', isAceptado=False)
        PorExamenDocumento.objects.create(porExamen=porExamen3, catTiposDocumento=catTiposDocumento2, documento='documento2', isAceptado=False)

        self.json = {
            "isAceptado": True
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        datos = PorExamenDocumento.objects.get(id=2)
        print(f'--->>>dato: {datos.id} - {datos.isAceptado}')
        response = self.client.put('/api/recertificacion/por-examen/documento/rechazar/2/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        # print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        datos = PorExamenDocumento.objects.get(id=2)
        print(f'--->>>dato: {datos.id} - {datos.isAceptado}')

        response = self.client.put('/api/recertificacion/por-examen/documento/rechazar/22/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> no encotrado 404 \n {json.dumps(response.json())} \n ---')
        # print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetPorExamenMedicoDetail200Test(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        PorExamen.objects.create(medico=medico9, estatus=3, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        PorExamen.objects.create(medico=medico6, estatus=2, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        PorExamen.objects.create(medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        PorExamen.objects.create(medico=medico9, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        PorExamen.objects.create(medico=medico9, estatus=3, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        PorExamen.objects.create(medico=medico6, estatus=2, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        PorExamen.objects.create(medico=medico6, estatus=2, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        PorExamen.objects.create(medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        PorExamen.objects.create(medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)
        PorExamen.objects.create(medico=medico9, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/por-examen/medico/9/detail/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/por-examen/medico/6/detail/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/por-examen/medico/66/detail/')
        print(f'response JSON ===>>> 404 no existe \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetDescargarExcel200Test(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=333)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=666)
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999)

        fechaExamen1 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-04-01', descripcion='primer fecha')
        fechaExamen2 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-08-01', descripcion='segunda fecha')
        fechaExamen3 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-12-01', descripcion='tercera fecha')

        PorExamen.objects.create(medico=medico9, estatus=3, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen2)  # 1
        PorExamen.objects.create(medico=medico6, estatus=2, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 2
        PorExamen.objects.create(medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 3

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/por-examen/fecha/1/bajar-excel/list/')
        print(f'response JSON ===>>> ok \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutProcesaExcel200Test(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=333)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=666)
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999)

        fechaExamen1 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-04-01', descripcion='primer fecha')
        fechaExamen2 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-08-01', descripcion='segunda fecha')
        fechaExamen3 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-12-01', descripcion='tercera fecha')

        PorExamen.objects.create(medico=medico9, estatus=3, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen2)  # 1
        PorExamen.objects.create(medico=medico6, estatus=2, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 2
        PorExamen.objects.create(medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 3

        archivo = open('./uploads/recertificacion.csv', 'rb')
        csvFile = SimpleUploadedFile(archivo.name, archivo.read(), content_type='text/csv')

        self.json = {
            "archivo": csvFile
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put('/api/recertificacion/por-examen/fecha/1/cargar-excel/update/', data=self.json, format='multipart')
        print(f'response JSON ===>>> ok \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        datos = PorExamen.objects.all()
        for dato in datos:
            print(f'--->>>id: {dato.id} - calificacion: {dato.calificacion}')


class GetPublicarCalificaciones200Test(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=333)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=666)
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999)

        fechaExamen1 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-04-01', descripcion='primer fecha')
        fechaExamen2 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-08-01', descripcion='segunda fecha')
        fechaExamen3 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-12-01', descripcion='tercera fecha')

        PorExamen.objects.create(medico=medico9, estatus=3, isAprobado=True, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1, isPublicado=False)  # 1
        PorExamen.objects.create(medico=medico6, estatus=2, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1, isPublicado=False)  # 2
        PorExamen.objects.create(medico=medico3, estatus=1, isAprobado=True, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1, isPublicado=False)  # 3

        archivo = open('./uploads/recertificacion.csv', 'rb')
        csvFile = SimpleUploadedFile(archivo.name, archivo.read(), content_type='text/csv')

        self.json = {
            "archivo": csvFile
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        cuentaCertificados = Certificado.objects.count()
        print(f'--->>>cuentaCertificados: {cuentaCertificados}')

        response = self.client.get('/api/recertificacion/por-examen/fecha/1/publicar/list/')
        print(f'response JSON ===>>> ok \n {response.content} \n ---')
        # print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        # print(f'response JSON ===>>> ok \n {response.json()} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cuentaCertificados = Certificado.objects.count()
        print(f'--->>>cuentaCertificados: {cuentaCertificados}')


class GetEnviarCorreoDocumentos200Test(APITestCase):
    def setUp(self):
        catTiposDocumento1 = CatTiposDocumento.objects.create(descripcion='Revalidación')
        catTiposDocumento2 = CatTiposDocumento.objects.create(descripcion='CURP')
        catTiposDocumento3 = CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        catTiposDocumento4 = CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        catTiposDocumento5 = CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        catTiposDocumento6 = CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        catTiposDocumento7 = CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        catTiposDocumento8 = CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        catTiposDocumento9 = CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        catTiposDocumento10 = CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')
        catTiposDocumento11 = CatTiposDocumento.objects.create(descripcion='Ficha de Registro')
        catTiposDocumento12 = CatTiposDocumento.objects.create(descripcion='Fotografía')
        catTiposDocumento13 = CatTiposDocumento.objects.create(descripcion='Certificado')

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=333)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=666)
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999)

        fechaExamen1 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-04-01', descripcion='primer fecha')
        fechaExamen2 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-08-01', descripcion='segunda fecha')
        fechaExamen3 = FechasExamenRecertificacion.objects.create(fechaExamen='2021-12-01', descripcion='tercera fecha')

        porExamen9 = PorExamen.objects.create(id=9, medico=medico9, estatus=3, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen2)  # 1
        porExamen6 = PorExamen.objects.create(id=6, medico=medico6, estatus=2, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 2
        porExamen3 = PorExamen.objects.create(id=3, medico=medico3, estatus=1, isAprobado=False, calificacion=0, isPagado=False, isAceptado=False, fechaExamen=fechaExamen1)  # 3

        PorExamenDocumento.objects.create(porExamen=porExamen9, catTiposDocumento=catTiposDocumento9, documento='documento9', isAceptado=True)
        PorExamenDocumento.objects.create(porExamen=porExamen9, catTiposDocumento=catTiposDocumento6, documento='documento6', isAceptado=True)
        # PorExamenDocumento.objects.create(porExamen=porExamen9, catTiposDocumento=catTiposDocumento3, documento='documento3', isAceptado=False)
        # PorExamenDocumento.objects.create(porExamen=porExamen6, catTiposDocumento=catTiposDocumento1, documento='documento1', isAceptado=False)
        # PorExamenDocumento.objects.create(porExamen=porExamen3, catTiposDocumento=catTiposDocumento2, documento='documento2', isAceptado=False)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        datos = PorExamen.objects.get(id=9)
        print(f'--->>>datos.id: {datos.id} - datos.isAceptado: {datos.isAceptado}')
        response = self.client.get('/api/recertificacion/por-examen/9/correo-documentos/')
        print(f'response JSON ===>>> ok 2  documentos aceptados \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        datos = PorExamen.objects.get(id=9)
        print(f'--->>>datos.id: {datos.id} - datos.isAceptado: {datos.isAceptado}')

        PorExamenDocumento.objects.filter(id=1).update(isAceptado=False)
        response = self.client.get('/api/recertificacion/por-examen/9/correo-documentos/')
        print(f'response JSON ===>>> ok 1 documento aceptado \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        datos = PorExamen.objects.get(id=9)
        print(f'--->>>datos.id: {datos.id} - datos.isAceptado: {datos.isAceptado}')


class GetFechasExamenesList200Test(APITestCase):
    def setUp(self):
        FechasExamenRecertificacion.objects.create(fechaExamen='2021-04-01', descripcion='primer fecha')
        FechasExamenRecertificacion.objects.create(fechaExamen='2021-08-01', descripcion='segunda fecha')
        FechasExamenRecertificacion.objects.create(fechaExamen='2021-12-01', descripcion='tercera fecha')

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/fechas-examen/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostFechasExamenes200Test(APITestCase):
    def setUp(self):
        FechasExamenRecertificacion.objects.create(fechaExamen='2021-04-01', descripcion='primer fecha')
        FechasExamenRecertificacion.objects.create(fechaExamen='2021-08-01', descripcion='segunda fecha')
        FechasExamenRecertificacion.objects.create(fechaExamen='2021-12-01', descripcion='tercera fecha')

        self.json = {
            "fechaExamen": "2021-04-06",
            "descripcion": "mi cumpleaños"
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/recertificacion/fechas-examen/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutFechasExamenes200Test(APITestCase):
    def setUp(self):
        FechasExamenRecertificacion.objects.create(fechaExamen='2021-04-01', descripcion='primer fecha')
        FechasExamenRecertificacion.objects.create(fechaExamen='2021-08-01', descripcion='segunda fecha')
        FechasExamenRecertificacion.objects.create(fechaExamen='2021-12-01', descripcion='tercera fecha')

        self.json = {
            "fechaExamen": "2021-04-06",
            "descripcion": "mi cumpleaños"
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/fechas-examen/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put('/api/recertificacion/fechas-examen/3/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/fechas-examen/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutProrrogaCertificadoTest(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=333)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=666)
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999)

        Certificado.objects.create(medico=medico6, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=1)
        Certificado.objects.create(medico=medico3, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=2)
        Certificado.objects.create(medico=medico9, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=1)
        Certificado.objects.create(medico=medico3, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=2)
        Certificado.objects.create(medico=medico6, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=1)
        Certificado.objects.create(medico=medico9, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=3, documento='ya_hay_algo.pdf')

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = Certificado.objects.get(id=3)
        print(f'--->>>datos: {dato.id} - {dato.fechaCertificacion}')

        response = self.client.put('/api/recertificacion/certificado/3/prorroga/9/update/')
        print(f'response JSON ===>>> ok \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Certificado.objects.get(id=3)
        print(f'--->>>datos: {dato.id} - {dato.fechaCertificacion}')

        print('\n')
        response = self.client.put('/api/recertificacion/certificado/33/prorroga/9/update/')
        print(f'response JSON ===>>> 404 \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RenovacionTest(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=333)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=666)
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999)

        Renovacion.objects.create(medico=medico3)
        Renovacion.objects.create(medico=medico6)

        self.json = {
            "medico": 9,
            "isPagado": False
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/recertificacion/renovacion/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> OK \n {json.dumps(response.data, ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/api/recertificacion/renovacion/medico/3/detail/')
        print(f'response JSON ===>>> OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class variosTest(APITestCase):
    def setUp(self):
        pass

    def test(self):
        # fecha = date.today()
        # print(f'--->>>fecha: {fecha}')
        # fechaStr = fecha + relativedelta(years=5)
        # print(f'--->>>fechaStr: {fechaStr}')
        # print(f'--->>>type: {type(fechaStr)}')

        # otra = datetime.date.today() + relativedelta(years=5)
        # print(f'--->>>otra: {otra}')
        # -----------------------------------------------------
        # medico1 = Medico.objects.create(
        #     id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
        #     deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        #     cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        #     telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=369)

        # Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=False, fechaCertificacion='2045-04-06', estatus=1)
        # datos = Certificado.objects.get(id=1)
        # print(f'--->>>fechaCertificacion: {datos.fechaCertificacion} - fechaCaducidad: {datos.fechaCaducidad}')

        # Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=False, estatus=1)
        # datos = Certificado.objects.get(id=2)
        # print(f'--->>>fechaCertificacion: {datos.fechaCertificacion} - fechaCaducidad: {datos.fechaCaducidad}')

        # Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=False, estatus=1,
        #                            fechaCertificacion='2045-04-06', fechaCaducidad='2051-04-06')
        # datos = Certificado.objects.get(id=3)
        # print(f'--->>>fechaCertificacion: {datos.fechaCertificacion} - fechaCaducidad: {datos.fechaCaducidad}')
        # -----------------------------------------------------

        # medico3 = Medico.objects.create(
        #     id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
        #     deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        #     cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        #     telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        # medico6 = Medico.objects.create(
        #     id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
        #     deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        #     cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        #     telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        # medico9 = Medico.objects.create(
        #     id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
        #     deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        #     cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        #     telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        # Certificado.objects.create(medico=medico9, documento='certificado_de_chingon3.PDF', descripcion='vigente(1) false', isVencido=False, fechaCertificacion='2016-06-06',
        #                            fechaCaducidad=date.today()+relativedelta(years=3), estatus=1)
        # Certificado.objects.create(medico=medico3, documento='certificado_de_chingon3.PDF', descripcion='vencido(3) true', isVencido=False, fechaCertificacion='2016-06-06',
        #                            fechaCaducidad=date.today()-relativedelta(days=66), estatus=1)
        # Certificado.objects.create(medico=medico6, documento='certificado_de_chingon2.PDF', descripcion='por vencer(2) false', isVencido=False, fechaCertificacion='2000-05-06',
        #                            fechaCaducidad=date.today()+relativedelta(days=364), estatus=1)
        # Certificado.objects.create(medico=medico3, documento='certificado_de_chingon1.PDF', descripcion='vencido(3) true', isVencido=False, fechaCertificacion='2021-04-06',
        #                            fechaCaducidad=date.today()-relativedelta(months=9), estatus=1)
        # Certificado.objects.create(medico=medico9, documento='certificado_de_chingon3.PDF', descripcion='vigente(1) false', isVencido=False, fechaCertificacion='2016-06-06',
        #                            fechaCaducidad=date.today()+relativedelta(years=1, months=3), estatus=1)
        # Certificado.objects.create(medico=medico6, documento='certificado_de_chingon3.PDF', descripcion='por vencer(2) false', isVencido=False, fechaCertificacion='2016-06-06',
        #                            fechaCaducidad=date.today()+relativedelta(days=159), estatus=1)

        # Certificado.objects.create(medico=medico6, documento='certificado_de_chingon3.PDF', descripcion='vencido(3) true', isVencido=False, fechaCertificacion='2016-06-06',
        #                            fechaCaducidad=date.today()-relativedelta(months=11), estatus=1)
        # Certificado.objects.create(medico=medico6, documento='certificado_de_chingon3.PDF', descripcion='vencido(3) true', isVencido=False, fechaCertificacion='2016-06-06',
        #                            fechaCaducidad=date.today()-relativedelta(days=1), estatus=1)
        # Certificado.objects.create(medico=medico6, documento='certificado_de_chingon3.PDF', descripcion='por vencer(2) false', isVencido=False, fechaCertificacion='2016-06-06',
        #                            fechaCaducidad=date.today()+relativedelta(days=99), estatus=1)
        # Certificado.objects.create(medico=medico6, documento='certificado_de_chingon3.PDF', descripcion='vigente(1) false', isVencido=False, fechaCertificacion='2016-06-06',
        #                            fechaCaducidad=date.today()+relativedelta(years=1, days=9), estatus=1)

        # # queryset = Certificado.objects.filter(isVencido=False).values_list('id', 'fechaCaducidad__year')
        # # # 1 vigente / 2 esta por vencer / 3 vencido
        # #         print('esta por vencer')
        # #         Certificado.objects.filter(id=dato[0]).update(estatus=2, isVencido=False)
        # #         print('vencido')
        # #         Certificado.objects.filter(id=dato[0]).update(estatus=3, isVencido=True)
        # #         print('vigente')
        # #         Certificado.objects.filter(id=dato[0]).update(estatus=1, isVencido=False)

        # # fecha = date.today()
        # # for dato in queryset:
        # #     resta = (fecha - dato[1]).days
        # #     print(f'--->>>dato: {dato[0]} -> {dato[1]} -> {resta} -> {type(resta)}')
        # #     if resta > 0:
        # #         print('vencido')
        # #     if (resta <= 0) and (resta >= -365):
        # #         print('por vencer')
        # #     if resta <= -366:
        # #         print('vigente')

        # cuentaVencidos = Certificado.objects.filter(isVencido=False, fechaCaducidad__lt=date.today()).update(estatus=3, isVencido=True)
        # cuentaVigentes = Certificado.objects.filter(isVencido=False, fechaCaducidad__gte=date.today()).update(estatus=1, isVencido=False)
        # cuentaPorVencer = Certificado.objects.filter(isVencido=False, fechaCaducidad__range=[date.today(), date.today()+relativedelta(years=1)]).update(estatus=2, isVencido=False)
        # print(f'---> cuenta: {cuentaVencidos}')
        # print(f'---> cuenta: {cuentaVigentes}')
        # print(f'---> cuenta: {cuentaPorVencer}')

        # # queryset = Certificado.objects.all().values_list('id', 'fechaCaducidad', 'estatus', 'isVencido', 'descripcion').order_by('id')
        # # for dato in queryset:
        # #     print(f'--->>>dato: {dato[0]} - {dato[1]} - {dato[2]} - {dato[3]} - {dato[4]}')

        # queryset = Certificado.objects.all().values_list('id', 'fechaCaducidad').order_by('-fechaCaducidad')[:10]
        # for dato in queryset:
        #     print(f'--->>>dato: {dato[0]} - {dato[1]}')
        # # --------------------------------------------------------

        # FechasExamenRecertificacion.objects.create(fechaExamen='2021-04-01', descripcion='primer fecha')
        # FechasExamenRecertificacion.objects.create(fechaExamen='2021-08-01', descripcion='segunda fecha')
        # FechasExamenRecertificacion.objects.create(fechaExamen='2021-12-01', descripcion='tercer fecha')

        # queryset = FechasExamenRecertificacion.objects.filter(fechaExamen__gte=date.today()).order_by('-fechaExamen')[:1]
        # queryset = FechasExamenRecertificacion.objects.filter(fechaExamen__gte=date.today())
        # queryset = FechasExamenRecertificacion.objects.filter(fechaExamen__gte=date.today()-relativedelta(months=2))

        try:
            fechaPrueba = '2021-02-11'
            queryset = FechasExamenRecertificacion.objects.filter(fechaExamen__gte=fechaPrueba)
            queryset = queryset.order_by('fechaExamen')[:1]
            for dato in queryset:
                print(f'---dato: {dato.fechaExamen} - {fechaPrueba} - {dato.descripcion}')

            fechaPrueba = '2021-04-06'
            queryset = FechasExamenRecertificacion.objects.filter(fechaExamen__gte=fechaPrueba)
            queryset = queryset.order_by('fechaExamen')[:1]
            for dato in queryset:
                print(f'---dato: {dato.fechaExamen} - {fechaPrueba} - {dato.descripcion}')

            fechaPrueba = '2021-11-10'
            queryset = FechasExamenRecertificacion.objects.filter(fechaExamen__gte=fechaPrueba)
            queryset = queryset.order_by('fechaExamen')[:1]
            print(f'--->queryset: {queryset[0].fechaExamen}')
            for dato in queryset:
                print(f'---dato: {dato.fechaExamen} - {fechaPrueba} - {dato.descripcion}')
        except Exception as e:
            print(f'putamadre un error: {str(e)}')
