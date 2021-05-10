from catalogos.models import *

from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json
from rest_framework import status

import decimal


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

        response = self.client.get('/api/catalogo/motivo-rechazo/steelers/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/catalogo/motivo-rechazo/fall/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# usado para corregir error de que json.dumps no puede mostrar los tipos Decimal, aqui regreso un float


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            # return str(o)
            return float(o)
        return super(DecimalEncoder, self).default(o)


class PostCatPagosTest(APITestCase):
    def setUp(self):

        self.json = {
            "descripcion": "descricpcion 6",
            "precio": 369.99,
            "tipo": 6,
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/catalogo/pagos/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> \n {json.dumps(response.data, cls=DecimalEncoder)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
