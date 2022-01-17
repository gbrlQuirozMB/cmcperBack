from django.test import TestCase
from .models import *
from datetime import date
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


def configDB():
    ctde1 = CatTiposDocumentoEntrega.objects.create(descripcion='Certificado1')
    ctde2 = CatTiposDocumentoEntrega.objects.create(descripcion='Certificado2')
    ctde3 = CatTiposDocumentoEntrega.objects.create(descripcion='Certificado3')

    EntregaFisica.objects.create(fechaEntrega=date.today(), catTiposDocumentoEntrega=ctde1, nombreRecibe='nombre de quien recibe1', libro=1, foja=1, archivo='ninguno', comentarios='ninguno')


# python manage.py test entregaFisica.tests.BaseDatosTest
class BaseDatosTest(APITestCase):
    def setUp(self):
        configDB()
        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        datos = EntregaFisica.objects.all()
        for dato in datos:
            print(f'--->>>id: {dato.id} - nombreRecibe: {dato.nombreRecibe} - fecha: {dato.fecha}')


# python manage.py test entregaFisica.tests.PostEntregaFisicaTest
class PostEntregaFisicaTest(APITestCase):
    def setUp(self):

        configDB()

        archivo = open('./uploads/testUnit.jpg', 'rb')
        archivoFile = SimpleUploadedFile(archivo.name, archivo.read(), content_type='image/jpg')

        self.json = {
            "fechaEntrega": "2021-01-01",
            "catTiposDocumentoEntrega": 1,
            "nombreRecibe": "Fulanito de tal hernandez",
            "libro": 3,
            "foja": 6,
            "archivo": archivoFile,
            "comentarios": "comentarios chidos",
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/entrega-fisica/create/', data=self.json, format='multipart')
        print(f'response JSON ===>>> ok \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # del self.json['nombreRecibe']
        # response = self.client.post('/api/entrega-fisica/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> ok \n {json.dumps(response.data)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
