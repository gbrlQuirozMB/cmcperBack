from convocatoria.models import Convocatoria
from preregistro.models import Medico
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from io import BytesIO, StringIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from .serializers import *
import json

from datetime import date

import requests

# Create your tests here.


class PutEsExtranjero200Test(APITestCase):
    def setUp(self):
        Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        self.json = {
            "isExtranjero": "False",
            "nacionalidad": "Indio"
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = Medico.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.nombre} - {dato.isExtranjero} - {dato.nacionalidad}')

        response = self.client.put('/api/convocatoria/medico/es-extranjero/1/', self.json)
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Medico.objects.get(id=1)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.nombre} - {dato.isExtranjero} - {dato.nacionalidad}')


class PutEstudioExtranjero200Test(APITestCase):
    def setUp(self):
        Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        self.json = {
            "estudioExtranjero": True,
            "escuelaExtranjero": "MIT"
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = Medico.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.nombre} - {dato.estudioExtranjero} - {dato.escuelaExtranjero}')

        response = self.client.put('/api/convocatoria/medico/estudio-extranjero/1/', self.json)
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Medico.objects.get(id=1)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.nombre} - {dato.estudioExtranjero} - {dato.escuelaExtranjero}')


class PostConvocatoria200Test(APITestCase):
    def setUp(self):

        self.json = {
            "fechaInicio": "2020-06-04",
            "fechaTermino": "2021-02-11",
            "fechaExamen": "2021-04-06",
            "horaExamen": "09:09",
            "nombre": "convocatoria chingona",
            "detalles": "detalles",
            "precio": 369.99,
            "sedes": [
                {"descripcion": "miSede3"},
                {"descripcion": "miSede6"}
            ],
            "tipoExamenes": [
                {"descripcion": "tipo9"}
            ]
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/convocatoria/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        print(f'\n --->>> checando la DB <<<---')

        print(f'\n --->>>#registros convocatoria: {Convocatoria.objects.count()}')
        print(f'\n --->>>#registros sede: {Sede.objects.count()}')
        print(f'\n --->>>#registros tipoExamenes: {TipoExamen.objects.count()}')

        print(f'\n --->>>nombre: {Convocatoria.objects.get().nombre}')
        print(f'\n --->>>sede1: {Sede.objects.get(id=1).descripcion}')
        print(f'\n --->>>sede2: {Sede.objects.get(id=2).descripcion}')
        print(f'\n --->>>tipoExamen1: {TipoExamen.objects.get(id=1).descripcion}')


class GetList200Test(APITestCase):
    def setUp(self):
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1', precio=333.33)
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',horaExamen='09:09', nombre='convocatoria chingona2', detalles='detalles1', precio=333.33)
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-03-11', fechaExamen='2021-04-06',horaExamen='09:09', nombre='convocatoria chingona3', detalles='detalles1', precio=333.33)
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',horaExamen='09:09', nombre='convocatoria chingona4', detalles='detalles1', precio=333.33)
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',horaExamen='09:09', nombre='convocatoria chingona5', detalles='detalles1', precio=333.33)
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-15', fechaExamen='2021-04-06',horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles1', precio=333.33)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/convocatoria/list/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

        # data = Convocatoria.objects.filter(fechaTermino__gte=date.today())
        # print(f'--->>>data: {data}')

class baseDatosTest(APITestCase):
    def setUp(self):
        convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09',
                                                   nombre='convocatoria chingona', archivo='pdfFile', banner='pngFile', detalles='detalles', precio=369.99)
        Sede.objects.create(descripcion='sede chingona', convocatoria=convocatoria)

    def test(self):
        datoConvocatoria = Convocatoria.objects.get(id=1)
        print(f'--->>>dato: {datoConvocatoria}')
        serializer = ConvocatoriaSerializer(data=datoConvocatoria)
        print(f'--->>>serializer: {serializer}')
        if serializer.is_valid():
            # print(f'--->>>dato: {serializer.data}')
            print(set(serializer.data.keys()))
        print(f'--->>>dato: {serializer.errors}')
