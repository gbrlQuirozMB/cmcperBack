from instituciones.models import *


from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import Permission, User

import json
from rest_framework import status


# Create your tests here.

class PostInstitucionTest(APITestCase):
    def setUp(self):

        self.json = {
            "nombreInstitucion": "nombre institucion 1",
            "rfc": "rfc 1",
            "contacto": "contacto 1",
            "telUno": "telUno 1",
            "telDos": "telDos 1",
            "telCelular": "telCelular 1",
            "email": "email 1",
            "pais": "pais 1",
            "estado": "estado 1",
            "ciudad": "ciudad 1",
            "deleMuni": "deleMuni 1",
            "colonia": "colonia 1",
            "calle": "calle 1",
            "cp": "cp 1",
            "numInterior": "Interior 1",
            "numExterior": "Exterior 1"
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/instituciones/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> ok \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetInstitucionFilteredListTest(APITestCase):
    def setUp(self):
        Institucion.objects.create(nombreInstitucion='nombre institucion 1', rfc='rfc 1', contacto='contacto 1', telUno='telUno 1', telDos='telDos 1', telCelular='telCelular 1', email='email 1',
                                   pais='pais 1', estado='estado 1', ciudad='ciudad 1', deleMuni='deleMuni 1', colonia='colonia 1', calle='calle 1', cp='cp 1', numInterior='Interior 1',
                                   numExterior='Exterior 1')
        Institucion.objects.create(nombreInstitucion='nombre institucion 2', rfc='rfc 2', contacto='contacto 2', telUno='telUno 2', telDos='telDos 2', telCelular='telCelular 2', email='email 2',
                                   pais='pais 2', estado='estado 2', ciudad='ciudad 2', deleMuni='deleMuni 2', colonia='colonia 2', calle='calle 2', cp='cp 2', numInterior='Interior 2',
                                   numExterior='Exterior 2')
        Institucion.objects.create(nombreInstitucion='nombre institucion 3', rfc='rfc 3', contacto='contacto 3', telUno='telUno 3', telDos='telDos 3', telCelular='telCelular 3', email='email 3',
                                   pais='pais 3', estado='estado 3', ciudad='ciudad 3', deleMuni='deleMuni 3', colonia='colonia 3', calle='calle 3', cp='cp 3', numInterior='Interior 3',
                                   numExterior='Exterior 3')

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/instituciones/list/?nombreInstitucionNS=nombre institucion 3')
        print(f'response JSON ===>>> nombreInstitucionNS=nombre institucion 3 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/instituciones/list/?contactoNS=contacto 1')
        print(f'response JSON ===>>> contactoNS=contacto 1 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetInstitucionDetailTest(APITestCase):
    def setUp(self):
        Institucion.objects.create(nombreInstitucion='nombre institucion 1', rfc='rfc 1', contacto='contacto 1', telUno='telUno 1', telDos='telDos 1', telCelular='telCelular 1', email='email 1',
                                   pais='pais 1', estado='estado 1', ciudad='ciudad 1', deleMuni='deleMuni 1', colonia='colonia 1', calle='calle 1', cp='cp 1', numInterior='Interior 1',
                                   numExterior='Exterior 1')
        Institucion.objects.create(nombreInstitucion='nombre institucion 2', rfc='rfc 2', contacto='contacto 2', telUno='telUno 2', telDos='telDos 2', telCelular='telCelular 2', email='email 2',
                                   pais='pais 2', estado='estado 2', ciudad='ciudad 2', deleMuni='deleMuni 2', colonia='colonia 2', calle='calle 2', cp='cp 2', numInterior='Interior 2',
                                   numExterior='Exterior 2')
        Institucion.objects.create(nombreInstitucion='nombre institucion 3', rfc='rfc 3', contacto='contacto 3', telUno='telUno 3', telDos='telDos 3', telCelular='telCelular 3', email='email 3',
                                   pais='pais 3', estado='estado 3', ciudad='ciudad 3', deleMuni='deleMuni 3', colonia='colonia 3', calle='calle 3', cp='cp 3', numInterior='Interior 3',
                                   numExterior='Exterior 3')

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/instituciones/3/detail/')
        print(f'response JSON ===>>> ok (3) \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/instituciones/33/detail/')
        print(f'response JSON ===>>> 404 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PutInstitucionTest(APITestCase):
    def setUp(self):
        Institucion.objects.create(nombreInstitucion='nombre institucion 1', rfc='rfc 1', contacto='contacto 1', telUno='telUno 1', telDos='telDos 1', telCelular='telCelular 1', email='email 1',
                                   pais='pais 1', estado='estado 1', ciudad='ciudad 1', deleMuni='deleMuni 1', colonia='colonia 1', calle='calle 1', cp='cp 1', numInterior='Interior 1',
                                   numExterior='Exterior 1')
        Institucion.objects.create(nombreInstitucion='nombre institucion 2', rfc='rfc 2', contacto='contacto 2', telUno='telUno 2', telDos='telDos 2', telCelular='telCelular 2', email='email 2',
                                   pais='pais 2', estado='estado 2', ciudad='ciudad 2', deleMuni='deleMuni 2', colonia='colonia 2', calle='calle 2', cp='cp 2', numInterior='Interior 2',
                                   numExterior='Exterior 2')
        Institucion.objects.create(nombreInstitucion='nombre institucion 3', rfc='rfc 3', contacto='contacto 3', telUno='telUno 3', telDos='telDos 3', telCelular='telCelular 3', email='email 3',
                                   pais='pais 3', estado='estado 3', ciudad='ciudad 3', deleMuni='deleMuni 3', colonia='colonia 3', calle='calle 3', cp='cp 3', numInterior='Interior 3',
                                   numExterior='Exterior 3')

        self.json = {
            "nombreInstitucion": "nombre institucion 66",
            "rfc": "rfc 66",
            "contacto": "contacto 66",
            "telUno": "telUno 66",
            "telDos": "telDos 66",
            "telCelular": "telCelular 66",
            "email": "email 66",
            "pais": "pais 66",
            "estado": "estado 66",
            "ciudad": "ciudad 66",
            "deleMuni": "deleMuni 66",
            "colonia": "colonia 66",
            "calle": "calle 66",
            "cp": "cp 66",
            "numInterior": "N Int 66",
            "numExterior": "N Ext 66"
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put('/api/instituciones/3/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> ok (3) \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put('/api/instituciones/33/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> 404 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteInstitucionTest(APITestCase):
    def setUp(self):
        Institucion.objects.create(nombreInstitucion='nombre institucion 1', rfc='rfc 1', contacto='contacto 1', telUno='telUno 1', telDos='telDos 1', telCelular='telCelular 1', email='email 1',
                                   pais='pais 1', estado='estado 1', ciudad='ciudad 1', deleMuni='deleMuni 1', colonia='colonia 1', calle='calle 1', cp='cp 1', numInterior='Interior 1',
                                   numExterior='Exterior 1')
        Institucion.objects.create(nombreInstitucion='nombre institucion 2', rfc='rfc 2', contacto='contacto 2', telUno='telUno 2', telDos='telDos 2', telCelular='telCelular 2', email='email 2',
                                   pais='pais 2', estado='estado 2', ciudad='ciudad 2', deleMuni='deleMuni 2', colonia='colonia 2', calle='calle 2', cp='cp 2', numInterior='Interior 2',
                                   numExterior='Exterior 2')
        Institucion.objects.create(nombreInstitucion='nombre institucion 3', rfc='rfc 3', contacto='contacto 3', telUno='telUno 3', telDos='telDos 3', telCelular='telCelular 3', email='email 3',
                                   pais='pais 3', estado='estado 3', ciudad='ciudad 3', deleMuni='deleMuni 3', colonia='colonia 3', calle='calle 3', cp='cp 3', numInterior='Interior 3',
                                   numExterior='Exterior 3')

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        cuenta = Institucion.objects.all().count()
        print(f'--->>>cuenta registros original: {cuenta}')

        response = self.client.delete('/api/instituciones/3/delete/')
        print(f'response JSON ===>>> ok 204 sin contenido \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete('/api/instituciones/33/delete/')
        print(f'response JSON ===>>> 404 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        cuenta = Institucion.objects.all().count()
        print(f'--->>>cuenta registros despues: {cuenta}')


class PutCorreoInstitucionTest(APITestCase):
    def setUp(self):
        Permission.objects.create(content_type_id=39, codename='add_actividadavaladaasistente', name='Can add actividad avalada asistente')
        Permission.objects.create(content_type_id=39, codename='change_actividadavaladaasistente', name='Can change actividad avalada asistente')
        Permission.objects.create(content_type_id=39, codename='delete_actividadavaladaasistente', name='Can delete actividad avalada asistente')
        Permission.objects.create(content_type_id=39, codename='view_actividadavaladaasistente', name='Can view actividad avalada asistente')
        
        Institucion.objects.create(nombreInstitucion='nombre institucion 1', rfc='rfc 1', contacto='contacto 1', telUno='telUno 1', telDos='telDos 1', telCelular='telCelular 1', email='email 1',
                                   pais='pais 1', estado='estado 1', ciudad='ciudad 1', deleMuni='deleMuni 1', colonia='colonia 1', calle='calle 1', cp='cp 1', numInterior='Interior 1',
                                   numExterior='Exterior 1')
        Institucion.objects.create(nombreInstitucion='nombre institucion 2', rfc='rfc 2', contacto='contacto 2', telUno='telUno 2', telDos='telDos 2', telCelular='telCelular 2', email='email 2',
                                   pais='pais 2', estado='estado 2', ciudad='ciudad 2', deleMuni='deleMuni 2', colonia='colonia 2', calle='calle 2', cp='cp 2', numInterior='Interior 2',
                                   numExterior='Exterior 2')
        Institucion.objects.create(nombreInstitucion='nombre institucion 3', rfc='rfc 3', contacto='contacto 3', telUno='telUno 3', telDos='telDos 3', telCelular='telCelular 3', email='email 3',
                                   pais='pais 3', estado='estado 3', ciudad='ciudad 3', deleMuni='deleMuni 3', colonia='colonia 3', calle='calle 3', cp='cp 3', numInterior='Interior 3',
                                   numExterior='Exterior 3')

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        datos = Institucion.objects.get(id=3)
        print(f'--->>>rfc: {datos.rfc} - username: {datos.username}')

        response = self.client.put('/api/instituciones/3/correo/')
        print(f'response JSON ===>>> ok (3) \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put('/api/instituciones/33/correo/')
        print(f'response JSON ===>>> 404 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        datos = Institucion.objects.get(id=3)
        print(f'--->>>rfc: {datos.rfc} - username: {datos.username} \n')

        cuenta = User.objects.count()
        # que el usuario se haya creado correctamente
        # self.assertEqual(User.objects.count(), 5)
        # self.assertEqual(User.objects.get(id=5).email, 'gabriel@mb.company')
        queryset = User.objects.filter(id=cuenta)
        for dato in queryset:
            print(f'username: {dato.username}')
            print(f'email: {dato.email}')
            print(f'password: {dato.password}')
            print(f'first_name: {dato.first_name}')
            print(f'last_name: {dato.last_name}')
            print(f'user_permissions: {dato.get_user_permissions()}')   
            print(f'is_staff: {dato.is_staff}')
