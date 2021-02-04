import json
from notificaciones.models import Notificacion

from django.contrib.auth.models import User
from preregistro.models import Medico
from django.http import response
from rest_framework import status
from rest_framework.test import APITestCase

nl = '\n'

# Create your tests here.

class PostUserData200Test(APITestCase):
    def setUp(self):
        User.objects.create_user(username='limitado',email='limitado@cmcper.com',password='password',first_name='Juanito',last_name='Perez')
        User.objects.create_user(username='normal',email='normal@cmcper.com',password='password',first_name='Panchito',last_name='Sanchez')
        User.objects.create_user(username='admin',email='admin@cmcper.com',password='password',first_name='Enrique',last_name='Lucero', is_superuser=True, is_staff=True)
        
        Medico.objects.create(id=3, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1', deleMuni='deleMuni1',
                              colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1', cedEspecialidad='cedEspecialidad1',
                              cedCirugiaGral='cedCirugiaGral1',hospitalResi='hospitalResi1',telJefEnse='telJefEnse1',fechaInicioResi='1999-06-06',fechaFinResi='2000-07-07',telCelular='telCelular1',
                              telParticular='telParticular1',email='gabriel@mb.company', username='limitado')
        self.json = {
            "username": "limitado",
            "password": "password"
        }
        
        # self.user = User.objects.create_user(username='gabriel') #IsAuthenticated
        
    
    def test(self):
        # self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/api-token-auth/',self.json)
        print(f'response JSON ===>>> {nl} {response.data} {nl} ---')