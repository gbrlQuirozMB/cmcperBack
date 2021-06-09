from instituciones.models import *
from actividadesAvaladas.models import *
from recertificacion.models import Capitulo, Subcapitulo, Item

from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import json
from rest_framework import status

from datetime import date
from dateutil.relativedelta import relativedelta


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

        print(f'\n --->>>ActividadAvalada.qrCodeImg: {ActividadAvalada.objects.get().qrCodeImg}')


class PutArchivoTest(APITestCase):
    def setUp(self):
        institucion1 = Institucion.objects.create(nombreInstitucion='nombre institucion 1', rfc='rfc 1', contacto='contacto 1', telUno='telUno 1', telDos='telDos 1', telCelular='telCelular 1',
                                                  email='email 1', pais='pais 1', estado='estado 1', ciudad='ciudad 1', deleMuni='deleMuni 1', colonia='colonia 1', calle='calle 1', cp='cp 1',
                                                  numInterior='Interior 1', numExterior='Exterior 1')

        capitulo1 = Capitulo.objects.create(titulo='titulo 1', descripcion='capitulo descripcion 1', puntos=33.0, maximo=50.0, minimo=50.0, isOpcional=False)
        subcapitulo1 = Subcapitulo.objects.create(descripcion='subcapitulo descripcion 1', comentarios='subcapitulo comentarios 1', capitulo=capitulo1)
        item1 = Item.objects.create(descripcion='item descripcion 1', puntos=3, subcapitulo=subcapitulo1)

        ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.3,
                                        fechaInicio=date.today()+relativedelta(days=8), lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1')

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

        ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.3,
                                        fechaInicio=date.today()+relativedelta(days=8), lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1')

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

        ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.1, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion1, item=item2, nombre='nombre 2', emailContacto='emailContacto 2', numAsistentes=9, puntosAsignar=3.2, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 2', solicitante='solicitante 2', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 2', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion2, item=item3, nombre='nombre 3', emailContacto='emailContacto 3', numAsistentes=9, puntosAsignar=3.3, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 3', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion2, item=item4, nombre='nombre 4', emailContacto='emailContacto 4', numAsistentes=9, puntosAsignar=3.4, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 4', solicitante='solicitante 4', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 4', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion3, item=item5, nombre='nombre 5', emailContacto='emailContacto 5', numAsistentes=9, puntosAsignar=3.5, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 5', solicitante='solicitante 5', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 5', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion3, item=item6, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 6', solicitante='solicitante 6', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 6', isPagado=True)

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

        ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.1, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion1, item=item2, nombre='nombre 2', emailContacto='emailContacto 2', numAsistentes=9, puntosAsignar=3.2, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 2', solicitante='solicitante 2', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 2', isPagado=True)
        aa3 = ActividadAvalada.objects.create(institucion=institucion2, item=item3, nombre='nombre 3', emailContacto='emailContacto 3', numAsistentes=9, puntosAsignar=3.3, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 3', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion2, item=item4, nombre='nombre 4', emailContacto='emailContacto 4', numAsistentes=9, puntosAsignar=3.4, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 4', solicitante='solicitante 4', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 4', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion3, item=item5, nombre='nombre 5', emailContacto='emailContacto 5', numAsistentes=9, puntosAsignar=3.5, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 5', solicitante='solicitante 5', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 5', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion3, item=item6, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 6', solicitante='solicitante 6', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 6', isPagado=True)

        Tema.objects.create(nombre='tema nombre 1', actividadAvalada=aa3)
        Tema.objects.create(nombre='tema nombre 2', actividadAvalada=aa3)
        Tema.objects.create(nombre='tema nombre 3', actividadAvalada=aa3)

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

        ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.1, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion1, item=item2, nombre='nombre 2', emailContacto='emailContacto 2', numAsistentes=9, puntosAsignar=3.2, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 2', solicitante='solicitante 2', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 2', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion2, item=item3, nombre='nombre 3', emailContacto='emailContacto 3', numAsistentes=9, puntosAsignar=3.3, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 3', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion2, item=item4, nombre='nombre 4', emailContacto='emailContacto 4', numAsistentes=9, puntosAsignar=3.4, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 4', solicitante='solicitante 4', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 4', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion3, item=item5, nombre='nombre 5', emailContacto='emailContacto 5', numAsistentes=9, puntosAsignar=3.5, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 5', solicitante='solicitante 5', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 5', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion3, item=item6, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 6', solicitante='solicitante 6', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 6', isPagado=True)

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

        print(f'\n --->>>ActividadAvalada.qrCodeImg: {ActividadAvalada.objects.get(id=3).qrCodeImg}')
        
        response = self.client.put('/api/actividades-avaladas/3/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> nombreNS=nombre 6 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put('/api/actividades-avaladas/33/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> institucionNS=nombre institucion 3 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        print(f'\n --->>>ActividadAvalada.qrCodeImg: {ActividadAvalada.objects.get(id=3).qrCodeImg}')
        
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

        ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.1, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion1, item=item2, nombre='nombre 2', emailContacto='emailContacto 2', numAsistentes=9, puntosAsignar=3.2, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 2', solicitante='solicitante 2', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 2', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion2, item=item3, nombre='nombre 3', emailContacto='emailContacto 3', numAsistentes=9, puntosAsignar=3.3, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 3', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion2, item=item4, nombre='nombre 4', emailContacto='emailContacto 4', numAsistentes=9, puntosAsignar=3.4, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 4', solicitante='solicitante 4', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 4', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion3, item=item5, nombre='nombre 5', emailContacto='emailContacto 5', numAsistentes=9, puntosAsignar=3.5, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 5', solicitante='solicitante 5', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 5', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion3, item=item6, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 6', solicitante='solicitante 6', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 6', isPagado=True)

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


class PostAsistenteActividadAvaladaTest(APITestCase):
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
        item4 = Item.objects.create(descripcion='item descripcion 1', puntos=10, subcapitulo=subcapitulo4)
        item5 = Item.objects.create(descripcion='item descripcion 2', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 3', puntos=30, subcapitulo=subcapitulo2)

        aa1 = ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.1,
                                              fechaInicio=date.today()+relativedelta(days=5), lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69,
                                              descripcion='descripcion 1', isPagado=False)

        aa2 = ActividadAvalada.objects.create(institucion=institucion1, item=item2, nombre='nombre 2', emailContacto='emailContacto 2', numAsistentes=9, puntosAsignar=3.2,
                                              fechaInicio=date.today()+relativedelta(days=8), lugar='lugar 2', solicitante='solicitante 2', tipoPago=1, porcentaje=1, precio=369.69,
                                              descripcion='descripcion 2', isPagado=True)

        self.aa3 = ActividadAvalada.objects.create(institucion=institucion2, item=item3, nombre='nombre 3', emailContacto='emailContacto 3', numAsistentes=3, puntosAsignar=3.3,
                                                   fechaInicio=date.today()+relativedelta(days=3), lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=1, precio=369.69,
                                                   descripcion='descripcion 3', isPagado=False)

        aa4 = ActividadAvalada.objects.create(institucion=institucion2, item=item4, nombre='nombre 4', emailContacto='emailContacto 4', numAsistentes=9, puntosAsignar=3.4,
                                              fechaInicio=date.today()+relativedelta(days=9), lugar='lugar 4', solicitante='solicitante 4', tipoPago=1, porcentaje=1, precio=369.69,
                                              descripcion='descripcion 4', isPagado=True)

        aa6 = ActividadAvalada.objects.create(id=6, institucion=institucion3, item=item5, nombre='nombre 5', emailContacto='emailContacto 5', numAsistentes=9, puntosAsignar=3.5,
                                              fechaInicio=date.today()+relativedelta(days=10), lugar='lugar 5', solicitante='solicitante 5', tipoPago=1, porcentaje=1, precio=369.69,
                                              descripcion='descripcion 5', isPagado=False)

        aa9 = ActividadAvalada.objects.create(id=9, institucion=institucion3, item=item6, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6,
                                              fechaInicio=date.today()+relativedelta(days=1), lugar='lugar 6', solicitante='solicitante 6', tipoPago=1, porcentaje=1, precio=369.69,
                                              descripcion='descripcion 6', isPagado=True)

        medico3 = Medico.objects.create(
            id=3, nombre='roberto', apPaterno='quiroz', apMaterno='tolentino', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=333, aceptado=True)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=666, aceptado=False)
        self.medico9 = Medico.objects.create(
            id=9, nombre='juan gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999, aceptado=True)

        AsistenteActividadAvalada.objects.create(medico=medico6, actividadAvalada=aa6)
        AsistenteActividadAvalada.objects.create(medico=self.medico9, actividadAvalada=aa9)
        AsistenteActividadAvalada.objects.create(medico=medico6, actividadAvalada=self.aa3)
        # AsistenteActividadAvalada.objects.create(medico=medico9, actividadAvalada=aa3)

        self.json = {
            "medico": 3,
            "actividadAvalada": 3
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/actividades-avaladas/3/asistentes/cupos/')
        print(f'response JSON ===>>> cupos \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/actividades-avaladas/333/asistentes/cupos/')
        print(f'response JSON ===>>> cupos 404 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # ------------CUPOS

        response = self.client.get('/api/actividades-avaladas/medicos/list/?nombreNS=gabr')
        print(f'response JSON ===>>> nombreNS=gabr\n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/actividades-avaladas/medicos/list/?nombreNS=gabriel')
        print(f'response JSON ===>>> nombreNS=gabriel \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # ------------BUSQUEDAS PARA AGREGAR

        response = self.client.post('/api/actividades-avaladas/asistente/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/api/actividades-avaladas/asistente/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> 409 medico ya registrado \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        AsistenteActividadAvalada.objects.create(medico=self.medico9, actividadAvalada=self.aa3)  # se agrega para llenar el cupo
        response = self.client.post('/api/actividades-avaladas/asistente/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> 409 cupo lleno \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        # ------------AGREGAR y VARIAS BL

        self.json = {
            "medico": 3,
            "actividadAvalada": 333
        }
        response = self.client.post('/api/actividades-avaladas/asistente/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> 404 no existe actividad avalada\n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.json = {
            "medico": 333,
            "actividadAvalada": 3
        }
        AsistenteActividadAvalada.objects.filter(id=3).delete()
        response = self.client.post('/api/actividades-avaladas/asistente/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> 400 no existe medico\n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # ---------------------------------------------------------
        # cuenta = AsistenteActividadAvalada.objects.all().count()
        # print(f'--->>>cuenta: {cuenta}')

        # datos = AsistenteActividadAvalada.objects.all()
        # for dato in datos:
        #     print(f'--->id: {dato.id} - medico: {dato.medico} - actividadAvalada: {dato.actividadAvalada}')

        # print(f'--->>>typeOf: {type(self.json)}')

        # nose=99
        # numAsistentes = ActividadAvalada.objects.filter(id=nose).values_list('numAsistentes', flat=True)
        # asistentesRegistrados = AsistenteActividadAvalada.objects.filter(actividadAvalada=nose).count()

        # if not numAsistentes:
        #     print(f'No existe actividad avalada')
        # else:
        #     print(f'--->>>{numAsistentes[0]}')

        # print(f'--->>>{asistentesRegistrados}')


class GetAsistenteActividadAvaladaFilteredListTest(APITestCase):
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
        item4 = Item.objects.create(descripcion='item descripcion 1', puntos=10, subcapitulo=subcapitulo4)
        item5 = Item.objects.create(descripcion='item descripcion 2', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 3', puntos=30, subcapitulo=subcapitulo2)

        aa1 = ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.1, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1', isPagado=False)
        aa2 = ActividadAvalada.objects.create(institucion=institucion1, item=item2, nombre='nombre 2', emailContacto='emailContacto 2', numAsistentes=9, puntosAsignar=3.2, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 2', solicitante='solicitante 2', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 2', isPagado=True)
        aa3 = ActividadAvalada.objects.create(institucion=institucion2, item=item3, nombre='nombre 3', emailContacto='emailContacto 3', numAsistentes=3, puntosAsignar=3.3, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 3', isPagado=False)
        aa4 = ActividadAvalada.objects.create(institucion=institucion2, item=item4, nombre='nombre 4', emailContacto='emailContacto 4', numAsistentes=9, puntosAsignar=3.4, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 4', solicitante='solicitante 4', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 4', isPagado=True)
        aa5 = ActividadAvalada.objects.create(institucion=institucion3, item=item5, nombre='nombre 5', emailContacto='emailContacto 5', numAsistentes=9, puntosAsignar=3.5, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 5', solicitante='solicitante 5', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 5', isPagado=False)
        aa6 = ActividadAvalada.objects.create(institucion=institucion3, item=item6, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 6', solicitante='solicitante 6', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 6', isPagado=True)

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='quiroz', apMaterno='tolentino', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='elianidTolentino@mb.company', numRegistro=333, aceptado=True)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='lauraCabrera@mb.company', numRegistro=666, aceptado=False)
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999, aceptado=True)

        AsistenteActividadAvalada.objects.create(medico=medico3, actividadAvalada=aa3)
        AsistenteActividadAvalada.objects.create(medico=medico6, actividadAvalada=aa3)
        AsistenteActividadAvalada.objects.create(medico=medico9, actividadAvalada=aa6)
        AsistenteActividadAvalada.objects.create(medico=medico9, actividadAvalada=aa1)
        AsistenteActividadAvalada.objects.create(medico=medico9, actividadAvalada=aa2)
        AsistenteActividadAvalada.objects.create(medico=medico9, actividadAvalada=aa4)

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/actividades-avaladas/asistentes/list/?nombreNS=gabriel')
        print(f'response JSON ===>>> nombreNS=gabriel \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/actividades-avaladas/asistentes/list/?apPaternoNS=quiroz&actividadAvalada=3')
        print(f'response JSON ===>>> apPaternoNS=quiroz&actividadAvalada=3 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/actividades-avaladas/asistentes/list/?apPaternoNS=quiroz&actividadAvalada=6')
        print(f'response JSON ===>>> apPaternoNS=quiroz&actividadAvalada=6 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteAsistenteActividadAvaladaTest(APITestCase):
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
        item4 = Item.objects.create(descripcion='item descripcion 1', puntos=10, subcapitulo=subcapitulo4)
        item5 = Item.objects.create(descripcion='item descripcion 2', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 3', puntos=30, subcapitulo=subcapitulo2)

        aa1 = ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.1, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1', isPagado=False)
        aa2 = ActividadAvalada.objects.create(institucion=institucion1, item=item2, nombre='nombre 2', emailContacto='emailContacto 2', numAsistentes=9, puntosAsignar=3.2, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 2', solicitante='solicitante 2', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 2', isPagado=True)
        aa3 = ActividadAvalada.objects.create(institucion=institucion2, item=item3, nombre='nombre 3', emailContacto='emailContacto 3', numAsistentes=3, puntosAsignar=3.3, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 3', isPagado=False)
        aa4 = ActividadAvalada.objects.create(institucion=institucion2, item=item4, nombre='nombre 4', emailContacto='emailContacto 4', numAsistentes=9, puntosAsignar=3.4, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 4', solicitante='solicitante 4', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 4', isPagado=True)
        aa5 = ActividadAvalada.objects.create(institucion=institucion3, item=item5, nombre='nombre 5', emailContacto='emailContacto 5', numAsistentes=9, puntosAsignar=3.5, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 5', solicitante='solicitante 5', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 5', isPagado=False)
        aa6 = ActividadAvalada.objects.create(institucion=institucion3, item=item6, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 6', solicitante='solicitante 6', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 6', isPagado=True)

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='quiroz', apMaterno='tolentino', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='elianidTolentino@mb.company', numRegistro=333, aceptado=True)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='lauraCabrera@mb.company', numRegistro=666, aceptado=False)
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999, aceptado=True)

        AsistenteActividadAvalada.objects.create(medico=medico3, actividadAvalada=aa3) 
        AsistenteActividadAvalada.objects.create(medico=medico6, actividadAvalada=aa3) 
        AsistenteActividadAvalada.objects.create(medico=medico9, actividadAvalada=aa6) 
        AsistenteActividadAvalada.objects.create(medico=medico9, actividadAvalada=aa1) 
        AsistenteActividadAvalada.objects.create(medico=medico9, actividadAvalada=aa2) 
        AsistenteActividadAvalada.objects.create(medico=medico9, actividadAvalada=aa4) 

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        cuenta = AsistenteActividadAvalada.objects.all().count()
        print(f'--->>>cuenta registros original: {cuenta}')
        datos = AsistenteActividadAvalada.objects.all().order_by('id')
        for dato in datos:
            print(f'--->>>id: {dato.id} - medico: {dato.medico.id} - actividadAvalada: {dato.actividadAvalada.id}')

        response = self.client.delete('/api/actividades-avaladas/asistente/3/delete/')
        print(f'response JSON ===>>> ok 204 sin contenido \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete('/api/actividades-avaladas/asistente/33/delete/')
        print(f'response JSON ===>>> 404 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        cuenta = AsistenteActividadAvalada.objects.all().count()
        print(f'--->>>cuenta registros despues: {cuenta}')
        datos = AsistenteActividadAvalada.objects.all().order_by('id')
        for dato in datos:
            print(f'--->>>id: {dato.id} - medico: {dato.medico.id} - actividadAvalada: {dato.actividadAvalada.id}')


class PutActividadAvaladaPagadoTest(APITestCase):
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

        ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.1, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion1, item=item2, nombre='nombre 2', emailContacto='emailContacto 2', numAsistentes=9, puntosAsignar=3.2, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 2', solicitante='solicitante 2', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 2', isPagado=True)
        aa3 = ActividadAvalada.objects.create(institucion=institucion2, item=item3, nombre='nombre 3', emailContacto='emailContacto 3', numAsistentes=9, puntosAsignar=3.3, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 3', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion2, item=item4, nombre='nombre 4', emailContacto='emailContacto 4', numAsistentes=9, puntosAsignar=3.4, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 4', solicitante='solicitante 4', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 4', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion3, item=item5, nombre='nombre 5', emailContacto='emailContacto 5', numAsistentes=9, puntosAsignar=3.5, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 5', solicitante='solicitante 5', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 5', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion3, item=item6, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 6', solicitante='solicitante 6', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 6', isPagado=True)

        Tema.objects.create(nombre='tema nombre 1', actividadAvalada=aa3)
        Tema.objects.create(nombre='tema nombre 2', actividadAvalada=aa3)
        Tema.objects.create(nombre='tema nombre 3', actividadAvalada=aa3)

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = ActividadAvalada.objects.get(id=3)
        print(f'--->>>ANTES dato: {dato.id} - {dato.isPagado}')

        response = self.client.put('/api/actividades-avaladas/3/pagado/')
        print(f'response JSON ===>>> ok\n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put('/api/actividades-avaladas/33/pagado/')
        print(f'response JSON ===>>> 404 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        dato = ActividadAvalada.objects.get(id=3)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.isPagado}')


class GetCostoAPagarTest(APITestCase):
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

        ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.1, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 1', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion1, item=item2, nombre='nombre 2', emailContacto='emailContacto 2', numAsistentes=9, puntosAsignar=3.2, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 2', solicitante='solicitante 2', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 2', isPagado=True)
        aa3 = ActividadAvalada.objects.create(institucion=institucion2, item=item3, nombre='nombre 3', emailContacto='emailContacto 3', numAsistentes=9, puntosAsignar=3.3, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=10, precio=369.69, descripcion='descripcion 3', isPagado=False)
        ActividadAvalada.objects.create(institucion=institucion2, item=item4, nombre='nombre 4', emailContacto='emailContacto 4', numAsistentes=9, puntosAsignar=3.4, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 4', solicitante='solicitante 4', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 4', isPagado=True)
        ActividadAvalada.objects.create(institucion=institucion3, item=item5, nombre='nombre 5', emailContacto='emailContacto 5', numAsistentes=9, puntosAsignar=3.5, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 5', solicitante='solicitante 5', tipoPago=1, porcentaje=1, precio=369.69, descripcion='descripcion 5', isPagado=False)
        aa6 = ActividadAvalada.objects.create(institucion=institucion3, item=item6, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6, fechaInicio=date.today(
        )+relativedelta(days=8), lugar='lugar 6', solicitante='solicitante 6', tipoPago=2, porcentaje=33, precio=0, descripcion='descripcion 6', isPagado=True)

        Tema.objects.create(nombre='tema nombre 1', actividadAvalada=aa3)
        Tema.objects.create(nombre='tema nombre 2', actividadAvalada=aa3)
        Tema.objects.create(nombre='tema nombre 3', actividadAvalada=aa3)

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # tipo=1->
        response = self.client.get('/api/actividades-avaladas/3/a-pagar/')
        print(f'response JSON ===>>> ok\n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get('/api/actividades-avaladas/6/a-pagar/')
        print(f'response JSON ===>>> ok\n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/actividades-avaladas/33/a-pagar/')
        print(f'response JSON ===>>> 404 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # dato = ActividadAvalada.objects.get(id=3)
        # print(f'--->>>DESPUES dato: {dato.id} - {dato.isPagado}')


class PostCargaMasivaExcelAsistenteActividadAvaladaTest(APITestCase):
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
        item4 = Item.objects.create(descripcion='item descripcion 1', puntos=10, subcapitulo=subcapitulo4)
        item5 = Item.objects.create(descripcion='item descripcion 2', puntos=20, subcapitulo=subcapitulo2)
        item6 = Item.objects.create(descripcion='item descripcion 3', puntos=30, subcapitulo=subcapitulo2)

        aa1 = ActividadAvalada.objects.create(institucion=institucion1, item=item1, nombre='nombre 1', emailContacto='emailContacto 1', numAsistentes=9, puntosAsignar=3.1,
                                              fechaInicio=date.today()+relativedelta(days=5), lugar='lugar 1', solicitante='solicitante 1', tipoPago=1, porcentaje=1, precio=369.69,
                                              descripcion='descripcion 1', isPagado=False)

        aa2 = ActividadAvalada.objects.create(institucion=institucion1, item=item2, nombre='nombre 2', emailContacto='emailContacto 2', numAsistentes=9, puntosAsignar=3.2,
                                              fechaInicio=date.today()+relativedelta(days=8), lugar='lugar 2', solicitante='solicitante 2', tipoPago=1, porcentaje=1, precio=369.69,
                                              descripcion='descripcion 2', isPagado=True)

        self.aa3 = ActividadAvalada.objects.create(institucion=institucion2, item=item3, nombre='nombre 3', emailContacto='emailContacto 3', numAsistentes=3, puntosAsignar=3.3,
                                                   fechaInicio=date.today()+relativedelta(days=3), lugar='lugar 3', solicitante='solicitante 3', tipoPago=1, porcentaje=1, precio=369.69,
                                                   descripcion='descripcion 3', isPagado=False)

        aa4 = ActividadAvalada.objects.create(institucion=institucion2, item=item4, nombre='nombre 4', emailContacto='emailContacto 4', numAsistentes=9, puntosAsignar=3.4,
                                              fechaInicio=date.today()+relativedelta(days=9), lugar='lugar 4', solicitante='solicitante 4', tipoPago=1, porcentaje=1, precio=369.69,
                                              descripcion='descripcion 4', isPagado=True)

        aa6 = ActividadAvalada.objects.create(id=6, institucion=institucion3, item=item5, nombre='nombre 5', emailContacto='emailContacto 5', numAsistentes=9, puntosAsignar=3.5,
                                              fechaInicio=date.today()+relativedelta(days=10), lugar='lugar 5', solicitante='solicitante 5', tipoPago=1, porcentaje=1, precio=369.69,
                                              descripcion='descripcion 5', isPagado=False)

        aa9 = ActividadAvalada.objects.create(id=9, institucion=institucion3, item=item6, nombre='nombre 6', emailContacto='emailContacto 6', numAsistentes=9, puntosAsignar=3.6,
                                              fechaInicio=date.today()+relativedelta(days=1), lugar='lugar 6', solicitante='solicitante 6', tipoPago=1, porcentaje=1, precio=369.69,
                                              descripcion='descripcion 6', isPagado=True)

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='nose', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=333, aceptado=True)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='bejarano', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=666, aceptado=False)
        self.medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999, aceptado=True)

        AsistenteActividadAvalada.objects.create(medico=medico6, actividadAvalada=aa6)
        AsistenteActividadAvalada.objects.create(medico=self.medico9, actividadAvalada=aa9)
        AsistenteActividadAvalada.objects.create(medico=medico6, actividadAvalada=self.aa3)

        archivo = open('./uploads/asistActiAvala.csv', 'rb')
        csvFile = SimpleUploadedFile(archivo.name, archivo.read(), content_type='text/csv')

        self.json = {
            "archivo": csvFile
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        cuenta = AsistenteActividadAvalada.objects.all().count()
        print(f'--->>>cuenta originales totales: {cuenta}')
        
        response = self.client.post('/api/actividades-avaladas/3/asistentes/cargar-excel/create/', data=self.json, format='multipart')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cuenta = AsistenteActividadAvalada.objects.all().count()
        print(f'--->>>cuenta: {cuenta}')
        
        datos = AsistenteActividadAvalada.objects.filter(actividadAvalada=3)
        for dato in datos:
            print(f'--->>>id: {dato.id} - medicoId: {dato.medico.id}')
            
        # se prueba que no permita  registros repetidos
        # se prueba que no existan medico en DB
        
        


class PruebaDiccionarios(APITestCase):
    def test(self):
        datos = {'dadosAlta':[]}
        valoReng = {'numCertificado': 0,'nombre':''}
        datos['dadosAlta'].append(valoReng)
        datos['dadosAlta'].append(valoReng)
        print(f'--->>>datos: {datos}')