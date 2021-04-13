from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


from preregistro.models import Medico
from recertificacion.models import *

from django.db.models import Sum

from datetime import date
from dateutil.relativedelta import relativedelta

from django.utils import timezone
import datetime


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

        # response = self.client.get('/api/recertificacion/all/all/0/list/') # regresa TODOS
        # print(f'response JSON ===>>> N:all - A:all - E:0 \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Medico.objects.filter(id=3).update(nombre='gabriel')
        # response = self.client.get('/api/recertificacion/gabriel/all/0/list/') # regresa gabriel quiroz y gabriel tolentino
        # print(f'response JSON ===>>> N:gabriel - A:all - E:0 \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Medico.objects.filter(id=3).update(nombre='laura', apPaterno='olvera')
        # Medico.objects.filter(id=9).update(apPaterno='olvera')
        # response = self.client.get('/api/recertificacion/all/olvera/0/list/') # regresa laura olvera y gabriel olvera
        # print(f'response JSON ===>>> N:all - A:olvera - E:0 \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/recertificacion/laura/all/2/list/') # regresa laura cabrera
        # print(f'response JSON ===>>> N:laura - A:all - E:2 \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/recertificacion/all/all/3/list/')  # regresa el que esta Pendiente
        print(f'response JSON ===>>> N:all - A:all - E:3 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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

        medico1 = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=369)

        Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=False, fechaCertificacion='2045-04-06', estatus=1)
        datos = Certificado.objects.get(id=1)
        print(f'--->>>fechaCertificacion: {datos.fechaCertificacion} - fechaCaducidad: {datos.fechaCaducidad}')

        Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=False, estatus=1)
        datos = Certificado.objects.get(id=2)
        print(f'--->>>fechaCertificacion: {datos.fechaCertificacion} - fechaCaducidad: {datos.fechaCaducidad}')

        Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=False, estatus=1,
                                   fechaCertificacion='2045-04-06', fechaCaducidad='2051-04-06')
        datos = Certificado.objects.get(id=3)
        print(f'--->>>fechaCertificacion: {datos.fechaCertificacion} - fechaCaducidad: {datos.fechaCaducidad}')
