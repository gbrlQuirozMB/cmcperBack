from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import *

from datetime import date
from dateutil.relativedelta import relativedelta

import json
from rest_framework import status

# Create your tests here.


def configDB():
    medico1 = Medico.objects.create(
        nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp3', fechaNac='2020-09-09', pais='pais3', estado='estado3', ciudad='ciudad3',
        deleMuni='deleMuni3', colonia='colonia', calle='calle3', cp='cp3', numExterior='numExterior3', rfcFacturacion='rfcFacturacion3', cedProfesional='cedProfesional3',
        cedEspecialidad='cedEspecialidad3', cedCirugiaGral='cedCirugiaGral3', hospitalResi='hospitalResi3', telJefEnse='telJefEnse3', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular3', telParticular='telParticular3', email='gabriel@mb.company', numRegistro=333, aceptado=True, telConsultorio='telConsultorio3', sexo='M',
        anioCertificacion=2022, isConsejero=True, isProfesor=False, isCertificado=False, estudioExtranjero=False, isExtranjero=False)
    medico2 = Medico.objects.create(
        nombre='elianid', apPaterno='tolentino', apMaterno='tolentino', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', email='elianid@mb.company', numRegistro=111, aceptado=True, telConsultorio='telConsultorio1', sexo='F',
        anioCertificacion=2022, isConsejero=True, isProfesor=False, isCertificado=True, estudioExtranjero=False, isExtranjero=False)

    encuesta1 = Encuesta.objects.create(titulo='titulo1', descripcion='descripcion', fechaInicio=date.today(), fechaFin=date.today() + relativedelta(days=8), estatus='Abierta',
                                        regionGeografica='Centro', isSoloConsejero=False)
    pregunta1 = Pregunta.objects.create(encuesta=encuesta1, descripcion='descripcionP', orden=1, hasOtro=False)
    opcion11 = Opcion.objects.create(pregunta=pregunta1, descripcion='descripcionO-1', orden=1)
    opcion12 = Opcion.objects.create(pregunta=pregunta1, descripcion='descripcionO-2', orden=2)
    pregunta2 = Pregunta.objects.create(encuesta=encuesta1, descripcion='descripcionP', orden=1, hasOtro=True)
    opcion21 = Opcion.objects.create(pregunta=pregunta2, descripcion='descripcionO-1', orden=1)
    opcion22 = Opcion.objects.create(pregunta=pregunta2, descripcion='descripcionO-2', orden=2)

    Respuesta.objects.create(opcion=opcion11, medico=medico1, fecha=date.today() + relativedelta(days=3), encuesta=encuesta1, pregunta=pregunta1)
    Respuesta.objects.create(opcion=opcion12, medico=medico1, fecha=date.today() + relativedelta(days=3), encuesta=encuesta1, pregunta=pregunta1)
    Respuesta.objects.create(opcion=opcion22, medico=medico1, fecha=date.today() + relativedelta(days=3), encuesta=encuesta1, pregunta=pregunta2)
    Respuesta.objects.create(medico=medico1, fecha=date.today() + relativedelta(days=3), otro='otroR', encuesta=encuesta1, pregunta=pregunta2)

    encuesta2 = Encuesta.objects.create(titulo='titulo1', descripcion='descripcion', fechaInicio=date.today(), fechaFin=date.today() + relativedelta(days=8), estatus='Cerrada',
                                        regionGeografica='Norte', isSoloConsejero=True)

# python manage.py test encuestas.tests.BaseDatosTest


class BaseDatosTest(APITestCase):
    def setUp(self):
        configDB()
        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # datos = EntregaFisica.objects.all()
        for dato in Encuesta.objects.all():
            print(f'Encuesta--->>>titulo: {dato.titulo} - fechaInicio: {dato.fechaInicio} - fechaFin: {dato.fechaFin} - estatus: {dato.estatus}')

        for dato in Pregunta.objects.all():
            print(f'Pregunta--->>>encuesta: {dato.encuesta} - descripcion: {dato.descripcion} - orden: {dato.orden} - estatus: {dato.hasOtro}')

        for dato in Opcion.objects.all():
            print(f'Opcion--->>>pregunta: {dato.pregunta} - descripcion: {dato.descripcion} - orden: {dato.orden}')

        for dato in Respuesta.objects.all():
            print(f'Respuesta--->>>opcion: {dato.opcion} - fecha: {dato.fecha} - otro: {dato.otro}')


# python manage.py test encuestas.tests.PostEncuestaTest
class PostEncuestaTest(APITestCase):
    def setUp(self):

        configDB()

        self.json = {
            "titulo": "tituloNew",
            "descripcion": "descripcionNew",
            "fechaInicio": date.today().strftime('%Y-%m-%d'),
            "fechaFin": (date.today() + relativedelta(days=8)).strftime('%Y-%m-%d'),
            "estatus": "Editar",
            "regionGeografica": "Centro",
            "isSoloConsejero": False
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)
        print(f'--->>>json: {self.json}')

        response = self.client.post('/api/encuestas/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> ok \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        del self.json['titulo']
        response = self.client.post('/api/encuestas/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> ok \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# python manage.py test encuestas.tests.GetEncuestaListTest
class GetEncuestaListTest(APITestCase):
    def setUp(self):

        configDB()

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/encuestas/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/encuestas/list/?estatus=Cerrada')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/encuestas/list/?regionGeografica=Norte')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/encuestas/list/?isSoloConsejero=true')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        fechaInicio = (date.today() + relativedelta(days=0)).strftime('%Y-%m-%d')
        fechaFin = (date.today() + relativedelta(days=8)).strftime('%Y-%m-%d')
        print(f'--->>>fechaInicio: {fechaInicio}')
        print(f'--->>>fechaFin: {fechaFin}')

        url = '/api/encuestas/list/?fechaInicioNS='+fechaInicio
        print(f'--->>>url: {url}')

        response = self.client.get(url)
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = '/api/encuestas/list/?fechaFinNS='+fechaFin
        print(f'--->>>url: {url}')

        response = self.client.get(url)
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# python manage.py test encuestas.tests.GetEncuestaDetailTest
class GetEncuestaDetailTest(APITestCase):
    def setUp(self):

        configDB()

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/encuestas/2/detail/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/encuestas/33/detail/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
