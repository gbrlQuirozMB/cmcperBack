from notificaciones.models import Notificacion
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User



# Create your tests here.
nl = '\n'

class GetNotificacionList200Test(APITestCase):
    def setUp(self):
        Notificacion.objects.create(titulo='titulo1',mensaje='mensaje1',destinatario=333,remitente=369)
        Notificacion.objects.create(titulo='titulo2',mensaje='mensaje2',destinatario=333,remitente=369)
        Notificacion.objects.create(titulo='titulo3',mensaje='mensaje3',destinatario=333,remitente=369,leido=True)
        Notificacion.objects.create(titulo='titulo4',mensaje='mensaje4',destinatario=333,remitente=369)
        Notificacion.objects.create(titulo='titulo5',mensaje='mensaje5',destinatario=333,remitente=369)
        Notificacion.objects.create(titulo='titulo6',mensaje='mensaje6',destinatario=666,remitente=369)
        Notificacion.objects.create(titulo='titulo7',mensaje='mensaje7',destinatario=666,remitente=369,leido=True)
        Notificacion.objects.create(titulo='titulo8',mensaje='mensaje8',destinatario=666,remitente=369,leido=True)
        Notificacion.objects.create(titulo='titulo9',mensaje='mensaje9',destinatario=666,remitente=369)
        Notificacion.objects.create(titulo='titulo10',mensaje='mensaje10',destinatario=666,remitente=369,leido=True)
        
        self.user = User.objects.create_user(username='gabriel') #IsAuthenticated
        
        
    def test(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/notificaciones/all/333/?orderby=creado_en&direc=asc')
        print(f'response JSON ===>>> \n {response.json()} \n ---')
        
        response = self.client.get('/api/notificaciones/all/666/?orderby=creado_en&direc=asc')
        print(f'response JSON ===>>> \n {response.json()} \n ---')      


class PutLeer200Test(APITestCase):
    def setUp(self):
        Notificacion.objects.create(titulo='titulo1',mensaje='mensaje1',destinatario=333,remitente=369)
        Notificacion.objects.create(titulo='titulo2',mensaje='mensaje2',destinatario=333,remitente=369)
        Notificacion.objects.create(titulo='titulo3',mensaje='mensaje3',destinatario=333,remitente=369)
        Notificacion.objects.create(titulo='titulo4',mensaje='mensaje4',destinatario=333,remitente=369)
        Notificacion.objects.create(titulo='titulo5',mensaje='mensaje5',destinatario=333,remitente=369)
            
    def test(self):
        response = self.client.put('/api/notificaciones/leer/3/')
        print(f'response JSON ===>>> {nl} {response.data} {nl} ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        dato = Notificacion.objects.get(id=3)
        print(f'--->>>dato: {dato.id} - {dato.leido}')
        
        # response = self.client.get('/api/notificaciones/all/333/?orderby=creado_en&direc=asc')
        # print(f'response JSON ===>>> \n {response.json()} \n ---')