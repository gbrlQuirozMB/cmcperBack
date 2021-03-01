from catalogos.models import *

from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json
from rest_framework import status


# Create your tests here.
class GetMotivoRechazo200Test(APITestCase):
    def setUp(self):
        CatMotivosRechazo.objects.create(descripcion='muchos fallos', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='no sirve', tipo=2)
        CatMotivosRechazo.objects.create(descripcion='perdieron los steelers', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='engargolado incorrecto', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='documento perdido', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='no se que mas poner fall', tipo=2)
        CatMotivosRechazo.objects.create(descripcion='ganaron los steelers', tipo=1)
        
        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    
    def test(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/catalogo/motivo-rechazo/steelers/')  # regresa TODOS
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get('/api/catalogo/motivo-rechazo/fall/')  # regresa TODOS
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)