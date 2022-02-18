from django.test import TestCase
from .models import *
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

import json
from rest_framework import status


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

    carpeta1 = Carpeta.objects.create(medico=medico1, nombre='carpeta1')
    carpeta2 = Carpeta.objects.create(medico=medico1, nombre='carpeta2')
    carpeta3 = Carpeta.objects.create(medico=medico2, nombre='carpeta3')

    Archivo.objects.create(carpeta=carpeta1, nombre='sexoso.jpg', archivo='sexoso.jpg')
    Archivo.objects.create(carpeta=carpeta1, nombre='fotos calientes.jpg', archivo='fot-Hot.jpg')
    Archivo.objects.create(carpeta=carpeta2, nombre='gatitas sexys.jpg', archivo='pussy.jpg')
    Archivo.objects.create(carpeta=carpeta3, nombre='juguetes sexuales.jpg', archivo='toys.jpg')
    Archivo.objects.create(carpeta=carpeta2, nombre='no se algo de sexo.jpg', archivo='unknow-sex.jpg')


# python manage.py test archivosCarpetas.tests.BaseDatosTest
class BaseDatosTest(APITestCase):
    def setUp(self):
        configDB()
        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        datos = Archivo.objects.all()
        for dato in datos:
            print(f'--->>>id: {dato.id} - carpeta: {dato.carpeta.nombre} - medico: {dato.carpeta.medico.nombre} - nombre: {dato.nombre} - archivo: {dato.archivo}')


# python manage.py test archivosCarpetas.tests.PostCarpetasTest
class PostCarpetasTest(APITestCase):
    def setUp(self):

        configDB()

        self.json = {
            "medico": 1,
            "nombre": "carpetaNew"
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)
        # print(f'--->>>json: {self.json}')

        response = self.client.post('/api/archivos-carpetas/carpeta/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> ok \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        del self.json['medico']
        response = self.client.post('/api/archivos-carpetas/carpeta/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> ok \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# python manage.py test archivosCarpetas.tests.GetCarpetaListTest
class GetCarpetaListTest(APITestCase):
    def setUp(self):

        configDB()

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/archivos-carpetas/carpeta/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# python manage.py test archivosCarpetas.tests.GetCarpetaDetailTest
class GetCarpetaDetailTest(APITestCase):
    def setUp(self):

        configDB()

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/archivos-carpetas/carpeta/2/detail/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


