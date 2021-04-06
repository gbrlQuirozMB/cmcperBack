from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json
from rest_framework import status


from preregistro.models import Medico
from recertificacion.models import *

from django.db.models import Sum

# Create your tests here.
class GetCertificadoDatos200Test(APITestCase):
    def setUp(self):
        medico1 = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=369)

        Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=False, anioCertificacion=2000)
        Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=True, anioCertificacion=2000)
        Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=True, anioCertificacion=2000)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/recertificacion/medico/1/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        Certificado.objects.filter(id=1).update(anioCertificacion=2021)  # para revisar que esta vigente
        response = self.client.get('/api/recertificacion/medico/1/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        Certificado.objects.filter(id=1).update(anioCertificacion=2017)  # para revisar que esta por vencer
        response = self.client.get('/api/recertificacion/medico/1/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetAvanceCapituloMedico200Test(APITestCase):
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
        