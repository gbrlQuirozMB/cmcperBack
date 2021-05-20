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
            # "temas": []
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

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

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

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = ActividadAvalada.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.nombre} - {dato.banner}')

        response = self.client.put('/api/actividades-avaladas/1/banner/', data=self.json, format='multipart')
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = ActividadAvalada.objects.get(id=1)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.nombre} - {dato.banner}')


class GetActividadAvaladaFilteredListTest(APITestCase):
    def setUp(self):
        institucion1 = Institucion.objects.create(nombreInstitucion='nombre institucion 1', rfc='rfc 1', contacto='contacto 1', telUno='telUno 1', telDos='telDos 1', telCelular='telCelular 1',
                                                  email='email 1', pais='pais 1', estado='estado 1', ciudad='ciudad 1', deleMuni='deleMuni 1', colonia='colonia 1', calle='calle 1', cp='cp 1',
                                                  numInterior='Interior 1', numExterior='Exterior 1')
        institucion2 = Institucion.objects.create(nombreInstitucion='nombre institucion 2', rfc='rfc 2', contacto='contacto 2', telUno='telUno 2', telDos='telDos 2', telCelular='telCelular 2',
                                                  email='email 2', pais='pais 2', estado='estado 2', ciudad='ciudad 2', deleMuni='deleMuni 2', colonia='colonia 2', calle='calle 2', cp='cp 2',
                                                  numInterior='Interior 2', numExterior='Exterior 2')
        institucion3 = Institucion.objects.create(nombreInstitucion='nombre institucion 3', rfc='rfc 3', contacto='contacto 3', telUno='telUno 3', telDos='telDos 3', telCelular='telCelular 3',
                                                  email='email 3', pais='pais 3', estado='estado 3', ciudad='ciudad 3', deleMuni='deleMuni 3', colonia='colonia 3', calle='calle 3', cp='cp 3',
                                                  numInterior='Interior 3', numExterior='Exterior 3')

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

        ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.1, fechaInicio='2021-04-06',
                                        lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion1, item=item2, nombre='nombre 2', emailContacto='emailContacto 2', numAsistentes=9, puntosAsignar=3.2, fechaInicio='2021-04-06',
                                        lugar='lugar 2', solicitante='solicitante 2', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 2', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion2, item=item3, nombre='nombre 3', emailContacto='emailContacto 3', numAsistentes=9, puntosAsignar=3.3, fechaInicio='2021-04-06',
                                        lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 3', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion2, item=item4, nombre='nombre 4', emailContacto='emailContacto 4', numAsistentes=9, puntosAsignar=3.4, fechaInicio='2021-04-06',
                                        lugar='lugar 4', solicitante='solicitante 4', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 4', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion3, item=item5, nombre='nombre 5', emailContacto='emailContacto 5', numAsistentes=9, puntosAsignar=3.5, fechaInicio='2021-04-06',
                                        lugar='lugar 5', solicitante='solicitante 5', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 5', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion3, item=item6, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6, fechaInicio='2021-04-06',
                                        lugar='lugar 6', solicitante='solicitante 6', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 6', isPagado=True)

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/actividades-avaladas/list/?nombreNS=nombre 6')
        print(f'response JSON ===>>> nombreNS=nombre 6 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/actividades-avaladas/list/?institucionNS=nombre institucion 3')
        print(f'response JSON ===>>> institucionNS=nombre institucion 3 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/actividades-avaladas/list/?pagado=False')
        print(f'response JSON ===>>> pagado=False\n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/actividades-avaladas/list/?institucionNS=nombre institucion 3&pagado=True')
        print(f'response JSON ===>>> pagado=True\n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetActividadAvaladaDetailTest(APITestCase):
    def setUp(self):
        institucion1 = Institucion.objects.create(nombreInstitucion='nombre institucion 1', rfc='rfc 1', contacto='contacto 1', telUno='telUno 1', telDos='telDos 1', telCelular='telCelular 1',
                                                  email='email 1', pais='pais 1', estado='estado 1', ciudad='ciudad 1', deleMuni='deleMuni 1', colonia='colonia 1', calle='calle 1', cp='cp 1',
                                                  numInterior='Interior 1', numExterior='Exterior 1')
        institucion2 = Institucion.objects.create(nombreInstitucion='nombre institucion 2', rfc='rfc 2', contacto='contacto 2', telUno='telUno 2', telDos='telDos 2', telCelular='telCelular 2',
                                                  email='email 2', pais='pais 2', estado='estado 2', ciudad='ciudad 2', deleMuni='deleMuni 2', colonia='colonia 2', calle='calle 2', cp='cp 2',
                                                  numInterior='Interior 2', numExterior='Exterior 2')
        institucion3 = Institucion.objects.create(nombreInstitucion='nombre institucion 3', rfc='rfc 3', contacto='contacto 3', telUno='telUno 3', telDos='telDos 3', telCelular='telCelular 3',
                                                  email='email 3', pais='pais 3', estado='estado 3', ciudad='ciudad 3', deleMuni='deleMuni 3', colonia='colonia 3', calle='calle 3', cp='cp 3',
                                                  numInterior='Interior 3', numExterior='Exterior 3')

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

        ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.1, fechaInicio='2021-04-06',
                                        lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion1, item=item2, nombre='nombre 2', emailContacto='emailContacto 2', numAsistentes=9, puntosAsignar=3.2, fechaInicio='2021-04-06',
                                        lugar='lugar 2', solicitante='solicitante 2', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 2', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion2, item=item3, nombre='nombre 3', emailContacto='emailContacto 3', numAsistentes=9, puntosAsignar=3.3, fechaInicio='2021-04-06',
                                        lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 3', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion2, item=item4, nombre='nombre 4', emailContacto='emailContacto 4', numAsistentes=9, puntosAsignar=3.4, fechaInicio='2021-04-06',
                                        lugar='lugar 4', solicitante='solicitante 4', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 4', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion3, item=item5, nombre='nombre 5', emailContacto='emailContacto 5', numAsistentes=9, puntosAsignar=3.5, fechaInicio='2021-04-06',
                                        lugar='lugar 5', solicitante='solicitante 5', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 5', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion3, item=item6, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6, fechaInicio='2021-04-06',
                                        lugar='lugar 6', solicitante='solicitante 6', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 6', isPagado=True)

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/actividades-avaladas/3/detail/')
        print(f'response JSON ===>>> nombreNS=nombre 6 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/actividades-avaladas/33/detail/')
        print(f'response JSON ===>>> institucionNS=nombre institucion 3 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PutActividadAvaladaTest(APITestCase):
    def setUp(self):
        institucion1 = Institucion.objects.create(nombreInstitucion='nombre institucion 1', rfc='rfc 1', contacto='contacto 1', telUno='telUno 1', telDos='telDos 1', telCelular='telCelular 1',
                                                  email='email 1', pais='pais 1', estado='estado 1', ciudad='ciudad 1', deleMuni='deleMuni 1', colonia='colonia 1', calle='calle 1', cp='cp 1',
                                                  numInterior='Interior 1', numExterior='Exterior 1')
        institucion2 = Institucion.objects.create(nombreInstitucion='nombre institucion 2', rfc='rfc 2', contacto='contacto 2', telUno='telUno 2', telDos='telDos 2', telCelular='telCelular 2',
                                                  email='email 2', pais='pais 2', estado='estado 2', ciudad='ciudad 2', deleMuni='deleMuni 2', colonia='colonia 2', calle='calle 2', cp='cp 2',
                                                  numInterior='Interior 2', numExterior='Exterior 2')
        institucion3 = Institucion.objects.create(nombreInstitucion='nombre institucion 3', rfc='rfc 3', contacto='contacto 3', telUno='telUno 3', telDos='telDos 3', telCelular='telCelular 3',
                                                  email='email 3', pais='pais 3', estado='estado 3', ciudad='ciudad 3', deleMuni='deleMuni 3', colonia='colonia 3', calle='calle 3', cp='cp 3',
                                                  numInterior='Interior 3', numExterior='Exterior 3')

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

        ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.1, fechaInicio='2021-04-06',
                                        lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion1, item=item2, nombre='nombre 2', emailContacto='emailContacto 2', numAsistentes=9, puntosAsignar=3.2, fechaInicio='2021-04-06',
                                        lugar='lugar 2', solicitante='solicitante 2', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 2', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion2, item=item3, nombre='nombre 3', emailContacto='emailContacto 3', numAsistentes=9, puntosAsignar=3.3, fechaInicio='2021-04-06',
                                        lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 3', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion2, item=item4, nombre='nombre 4', emailContacto='emailContacto 4', numAsistentes=9, puntosAsignar=3.4, fechaInicio='2021-04-06',
                                        lugar='lugar 4', solicitante='solicitante 4', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 4', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion3, item=item5, nombre='nombre 5', emailContacto='emailContacto 5', numAsistentes=9, puntosAsignar=3.5, fechaInicio='2021-04-06',
                                        lugar='lugar 5', solicitante='solicitante 5', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 5', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion3, item=item6, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6, fechaInicio='2021-04-06',
                                        lugar='lugar 6', solicitante='solicitante 6', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 6', isPagado=True)

        self.json = {
            "institucion": 3,
            "item": 9,
            "nombre": "nombre 33",
            "emailContacto": "emailContacto 33",
            "numAsistentes": 99,
            "puntosAsignar": 33.3,
            "fechaInicio": "2021-09-09",
            "lugar": "lugar 33",
            "solicitante": "solicitante 33",
            "tipoPago": 2,
            "porcentaje": 33,
            "precio": 69.33,
            "descripcion": "descripcion 33",
            "temas": [
                {"nombre": "nombre de tema 333-1"},
                {"nombre": "nombre de tema 333-2"},
                {"nombre": "nombre de tema 333-3"},
            ]
            # "temas": []
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put('/api/actividades-avaladas/3/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> nombreNS=nombre 6 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put('/api/actividades-avaladas/33/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> institucionNS=nombre institucion 3 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteActividadAvaladaTest(APITestCase):
    def setUp(self):
        institucion1 = Institucion.objects.create(nombreInstitucion='nombre institucion 1', rfc='rfc 1', contacto='contacto 1', telUno='telUno 1', telDos='telDos 1', telCelular='telCelular 1',
                                                  email='email 1', pais='pais 1', estado='estado 1', ciudad='ciudad 1', deleMuni='deleMuni 1', colonia='colonia 1', calle='calle 1', cp='cp 1',
                                                  numInterior='Interior 1', numExterior='Exterior 1')
        institucion2 = Institucion.objects.create(nombreInstitucion='nombre institucion 2', rfc='rfc 2', contacto='contacto 2', telUno='telUno 2', telDos='telDos 2', telCelular='telCelular 2',
                                                  email='email 2', pais='pais 2', estado='estado 2', ciudad='ciudad 2', deleMuni='deleMuni 2', colonia='colonia 2', calle='calle 2', cp='cp 2',
                                                  numInterior='Interior 2', numExterior='Exterior 2')
        institucion3 = Institucion.objects.create(nombreInstitucion='nombre institucion 3', rfc='rfc 3', contacto='contacto 3', telUno='telUno 3', telDos='telDos 3', telCelular='telCelular 3',
                                                  email='email 3', pais='pais 3', estado='estado 3', ciudad='ciudad 3', deleMuni='deleMuni 3', colonia='colonia 3', calle='calle 3', cp='cp 3',
                                                  numInterior='Interior 3', numExterior='Exterior 3')

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

        ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.1, fechaInicio='2021-04-06',
                                        lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion1, item=item2, nombre='nombre 2', emailContacto='emailContacto 2', numAsistentes=9, puntosAsignar=3.2, fechaInicio='2021-04-06',
                                        lugar='lugar 2', solicitante='solicitante 2', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 2', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion2, item=item3, nombre='nombre 3', emailContacto='emailContacto 3', numAsistentes=9, puntosAsignar=3.3, fechaInicio='2021-04-06',
                                        lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 3', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion2, item=item4, nombre='nombre 4', emailContacto='emailContacto 4', numAsistentes=9, puntosAsignar=3.4, fechaInicio='2021-04-06',
                                        lugar='lugar 4', solicitante='solicitante 4', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 4', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion3, item=item5, nombre='nombre 5', emailContacto='emailContacto 5', numAsistentes=9, puntosAsignar=3.5, fechaInicio='2021-04-06',
                                        lugar='lugar 5', solicitante='solicitante 5', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 5', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion3, item=item6, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6, fechaInicio='2021-04-06',
                                        lugar='lugar 6', solicitante='solicitante 6', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 6', isPagado=True)

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        cuenta = ActividadAvalada.objects.all().count()
        print(f'--->>>cuenta registros original: {cuenta}')

        response = self.client.delete('/api/actividades-avaladas/3/delete/')
        print(f'response JSON ===>>> ok 204 sin contenido \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete('/api/actividades-avaladas/33/delete/')
        print(f'response JSON ===>>> 404\n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        cuenta = ActividadAvalada.objects.all().count()
        print(f'--->>>cuenta registros despues: {cuenta}')
