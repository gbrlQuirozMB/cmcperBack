from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Permission, ContentType
from .models import *
from preregistro.models import *

from datetime import date
from dateutil.relativedelta import relativedelta

import json
from rest_framework import status


def configDB():
    ulimitado = User.objects.create_user(username='limitado', email='limitado@cmcper.com', password='password', first_name='Juanito', last_name='Perez',is_staff=False)
    uNormal = User.objects.create_user(username='normal', email='normal@cmcper.com', password='password', first_name='Panchito', last_name='Sanchez',is_staff=True)
    # uAdmin = User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

    ct1 = ContentType.objects.create(app_label='chingao', model='nada')
    Permission.objects.create(name='Can add nada', content_type=ct1, codename='add_nada')
    Permission.objects.create(name='Can change nada', content_type=ct1, codename='change_nada')
    Permission.objects.create(name='Can delete nada', content_type=ct1, codename='delete_nada')
    Permission.objects.create(name='Can view nada', content_type=ct1, codename='view_nada')

    permisoAdd = Permission.objects.get(codename='add_nada')
    permisoChange = Permission.objects.get(codename='change_nada')
    permisoDelete = Permission.objects.get(codename='delete_nada')
    permisoView = Permission.objects.get(codename='view_nada')

    uNormal.user_permissions.set([permisoAdd, permisoChange, permisoDelete, permisoView])

    # uNormal.user_permissions.set([permisoAdd])

    medico3 = Medico.objects.create(
        id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2023-03-03', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', numRegistro=333, diplomaConacem='Pone Dora', titulo='Dra.')
    medico6 = Medico.objects.create(
        id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2026-06-06', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', email='laura.cabrera@mb.company', numRegistro=666, diplomaConacem='GlandM Enormes', titulo='Dra.')
    medico9 = Medico.objects.create(
        id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2029-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999, diplomaConacem='Yo mero', titulo='Dr.')


# python manage.py test permisos.tests.GetPermisosTest
class GetPermisosTest(APITestCase):
    def setUp(self):

        configDB()

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/permisos/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# python manage.py test permisos.tests.GetUsuariosFilteredTest
class GetUsuariosFilteredTest(APITestCase):
    def setUp(self):

        configDB()

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/permisos/usuarios/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/permisos/usuarios/list/?username=normal')
        print(f'response JSON ===>>> username=normal \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/permisos/usuarios/list/?first_name=Panchito')
        print(f'response JSON ===>>> first_name=Panchito \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/permisos/usuarios/list/?last_name=Perez')
        print(f'response JSON ===>>> last_name=Perez \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/permisos/usuarios/list/?email=limitado')
        print(f'response JSON ===>>> email=limitado \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/permisos/usuarios/list/?is_staff=false')
        print(f'response JSON ===>>> email=limitado \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# python manage.py test permisos.tests.PutPermisosUsuariosTest
class PutPermisosUsuariosTest(APITestCase):
    def setUp(self):

        configDB()

        self.json = {
            "permisos": [
                "delete_nada", "view_nada"
            ]
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        print(f'--->>>json: {self.json}')
        # response = self.client.get('/api/permisos/usuarios/list/?nombreNS=Panchito')
        # print(f'response JSON ===>>> nombreNS=Panchito \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put('/api/permisos/usuarios/2/permisos/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# python manage.py test permisos.tests.GetUsuariosDetailTest
class GetUsuariosDetailTest(APITestCase):
    def setUp(self):

        configDB()

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/permisos/usuarios/2/detail/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# python manage.py test permisos.tests.PostUsuariosTest
class PostUsuariosTest(APITestCase):
    def setUp(self):

        configDB()

        self.json = {
            "username": "gabrielMB",
            "email": "gabriel@mb.company",
            "first_name": "Gabriel",
            "last_name": "Quiroz Olvera"
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/permisos/usuarios/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        queryset = User.objects.filter(username='gabrielMB')
        for dato in queryset:
            print(f'--->>>username: {dato.username}')
            print(f'--->>>password: {dato.password}')


# python manage.py test permisos.tests.PutUsuariosTest
class PutUsuariosTest(APITestCase):
    def setUp(self):

        configDB()

        self.json = {
            "username": "gabrielMB",
            "email": "gabriel@mb.company",
            "first_name": "Gabriel",
            "last_name": "Quiroz Olvera"
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/permisos/usuarios/2/detail/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put('/api/permisos/usuarios/2/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# python manage.py test permisos.tests.DeleteUsuariosDetailTest
class DeleteUsuariosDetailTest(APITestCase):
    def setUp(self):

        configDB()

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # # existe el usuario
        # queryset = User.objects.filter(id=2)
        # for dato in queryset:
        #     print(f'\nusername: {dato.username}')
        #     print(f'email: {dato.email}')
        #     print(f'password: {dato.password}')
        #     print(f'first_name: {dato.first_name}')
        #     print(f'last_name: {dato.last_name}')
        #     print(f'user_permissions: {dato.get_user_permissions()}')

        # # existen los permisos
        # queryset = Permission.objects.filter(codename__contains='nada')
        # for dato in queryset:
        #     print(f'\nname: {dato.name}')
        #     print(f'codename: {dato.codename}')

        response = self.client.delete('/api/permisos/usuarios/2/delete/')
        print(f'response JSON ===>>> ok 204 sin contenido \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete('/api/permisos/usuarios/2/delete/')
        print(f'response JSON ===>>> ok 204 sin contenido \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # # existen los permisos
        # queryset = Permission.objects.filter(codename__contains='nada')
        # for dato in queryset:
        #     print(f'\nname: {dato.name}')
        #     print(f'codename: {dato.codename}')


# python manage.py test permisos.tests.DataBaseTest
class DataBaseTest(APITestCase):
    def setUp(self):

        configDB()

    def test(self):

        queryset = User.objects.filter()
        for dato in queryset:
            print(f'\nusername: {dato.username}')
            print(f'email: {dato.email}')
            print(f'password: {dato.password}')
            print(f'first_name: {dato.first_name}')
            print(f'last_name: {dato.last_name}')
            print(f'user_permissions: {dato.get_user_permissions()}')
