from instituciones.models import *


from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json
from rest_framework import status


# Create your tests here.

class PostInstitucionTest(APITestCase):
    def setUp(self):

        self.json = {
            "nombreInstitucion": "nombre institucion 1",
            "rfc": "rfc 1 ",
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
            "numExterior": "Exterior 1",
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/instituciones/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
