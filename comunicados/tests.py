from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import json
from rest_framework import status

from comunicados.models import *


# Create your tests here.
class PostComunicadoTest(APITestCase):
    def setUp(self):
        archivo = open('./uploads/testUnit.png', 'rb')
        imgFile = SimpleUploadedFile(archivo.name, archivo.read(), content_type='image/png')

        self.json = {
            "titulo": "titulo 3",
            "categoria": 3,
            "imagen": imgFile,
            "detalles": "detalles 3",
            "isActivo": True
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/comunicados/create/', data=self.json, format='multipart')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetComunicadoFilteredListTest(APITestCase):
    def setUp(self):
        Comunicado.objects.create(titulo='titulo1', categoria=1, imagen='imagen1.img', detalles='detalles1', isActivo=True)
        Comunicado.objects.create(titulo='titulo2', categoria=2, imagen='imagen2.img', detalles='detalles2', isActivo=True)
        Comunicado.objects.create(titulo='titulo3', categoria=3, imagen='imagen3.img', detalles='detalles3', isActivo=True)
        Comunicado.objects.create(titulo='titulo4', categoria=1, imagen='imagen4.img', detalles='detalles4', isActivo=True)
        Comunicado.objects.create(titulo='titulo5', categoria=3, imagen='imagen5.img', detalles='detalles5', isActivo=True)
        Comunicado.objects.create(titulo='titulo6', categoria=3, imagen='imagen6.img', detalles='detalles6', isActivo=True)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/comunicados/list/?tituloNS=titulo1')
        print(f'response JSON ===>>> tituloNS=titulo1 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/comunicados/list/?categoria=3')
        print(f'response JSON ===>>> categoria=3 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/comunicados/list/?tituloNS=titulo6&categoria=3')
        print(f'response JSON ===>>> tituloNS=titulo6&categoria=3 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetComunicadoDetailTest(APITestCase):
    def setUp(self):
        Comunicado.objects.create(titulo='titulo1', categoria=1, imagen='imagen1.img', detalles='detalles1', isActivo=True)
        Comunicado.objects.create(titulo='titulo2', categoria=2, imagen='imagen2.img', detalles='detalles2', isActivo=True)
        Comunicado.objects.create(titulo='titulo3', categoria=3, imagen='imagen3.img', detalles='detalles3', isActivo=True)
        Comunicado.objects.create(titulo='titulo4', categoria=1, imagen='imagen4.img', detalles='detalles4', isActivo=True)
        Comunicado.objects.create(titulo='titulo5', categoria=3, imagen='imagen5.img', detalles='detalles5', isActivo=True)
        Comunicado.objects.create(titulo='titulo6', categoria=3, imagen='imagen6.img', detalles='detalles6', isActivo=True)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/comunicados/3/detail/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/comunicados/33/detail/')
        print(f'response JSON ===>>> 404 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
