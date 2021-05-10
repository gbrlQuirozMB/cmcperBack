from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import json
from rest_framework import status


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
