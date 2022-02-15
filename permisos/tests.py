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
    ulimitado = User.objects.create_user(username='limitado', email='limitado@cmcper.com', password='password', first_name='Juanito', last_name='Perez')
    uNormal = User.objects.create_user(username='normal', email='normal@cmcper.com', password='password', first_name='Panchito', last_name='Sanchez')
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
