from instituciones.models import *
from actividadesAvaladas.models import *
from recertificacion.models import Capitulo, Subcapitulo, Item

from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import json
from rest_framework import status


# Create your tests here.

class PostActividadAvaladaTest(APITestCase):
    def setUp(self):
        Institucion.objects.create(nombreInstitucion='nombre institucion 1', rfc='rfc 1', contacto='contacto 1', telUno='telUno 1', telDos='telDos 1', telCelular='telCelular 1', email='email 1',
                                   pais='pais 1', estado='estado 1', ciudad='ciudad 1', deleMuni='deleMuni 1', colonia='colonia 1', calle='calle 1', cp='cp 1', numInterior='Interior 1',
                                   numExterior='Exterior 1')

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

        self.json = {
            "institucion": 1,
            "item": 1,
            "nombre": "nombre 1",
            "emailContacto": "emailContacto 1",
            "numAsistentes": 9,
            "puntosAsignar": 3.3,
            "fechaInicio": "2021-04-06",
            "lugar": "lugar 1",
            "solicitante": "solicitante 1",
            "tipoPago": 1,
            "porcentaje": 1,
            "precio": 369.69,
            "descripcion": "descripcion 1",
            "temas": [
                {"nombre": "nombre de tema 1"},
                {"nombre": "nombre de tema 2"},
                {"nombre": "nombre de tema 3"},
            ]
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/actividades-avaladas/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        print(f'\n --->>> checando la DB <<<---')

        print(f'\n --->>>#registros ActividadAvalada: {ActividadAvalada.objects.count()}')
        print(f'\n --->>>#registros Temas: {Tema.objects.count()}')

        print(f'\n --->>>ActividadAvalada.nombre: {ActividadAvalada.objects.get().nombre}')
        if Tema.objects.count() > 0:
            print(f'\n --->>>Tema.nombre: {Tema.objects.get(id=1).nombre}')
            print(f'\n --->>>Tema.nombre: {Tema.objects.get(id=2).nombre}')
            print(f'\n --->>>Tema.nombre: {Tema.objects.get(id=3).nombre}')


class PutArchivoTest(APITestCase):
    def setUp(self):
        institucion1 = Institucion.objects.create(nombreInstitucion='nombre institucion 1', rfc='rfc 1', contacto='contacto 1', telUno='telUno 1', telDos='telDos 1', telCelular='telCelular 1',
                                                  email='email 1', pais='pais 1', estado='estado 1', ciudad='ciudad 1', deleMuni='deleMuni 1', colonia='colonia 1', calle='calle 1', cp='cp 1',
                                                  numInterior='Interior 1', numExterior='Exterior 1')

        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)

        ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.3, fechaInicio='2021-04-06',
                                        lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1')

        archivo = open('./uploads/testUnit.pdf', 'rb')
        archivoFile = SimpleUploadedFile(archivo.name, archivo.read(), content_type='application/pdf')

        self.json = {
            "archivo": archivoFile
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = ActividadAvalada.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.nombre} - {dato.archivo}')

        response = self.client.put('/api/actividades-avaladas/1/archivo/', data=self.json, format='multipart')
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = ActividadAvalada.objects.get(id=1)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.nombre} - {dato.archivo}')


class PutBannerTest(APITestCase):
    def setUp(self):
        institucion1 = Institucion.objects.create(nombreInstitucion='nombre institucion 1', rfc='rfc 1', contacto='contacto 1', telUno='telUno 1', telDos='telDos 1', telCelular='telCelular 1',
                                                  email='email 1', pais='pais 1', estado='estado 1', ciudad='ciudad 1', deleMuni='deleMuni 1', colonia='colonia 1', calle='calle 1', cp='cp 1',
                                                  numInterior='Interior 1', numExterior='Exterior 1')

        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)

        ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.3, fechaInicio='2021-04-06',
                                        lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1')

        banner = open('./uploads/testUnit.jpg', 'rb')
        bannerFile = SimpleUploadedFile(banner.name, banner.read(), content_type='image/jpg')

        self.json = {
            "banner": bannerFile
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = ActividadAvalada.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.nombre} - {dato.banner}')

        response = self.client.put('/api/actividades-avaladas/1/banner/', data=self.json, format='multipart')
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = ActividadAvalada.objects.get(id=1)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.nombre} - {dato.banner}')
