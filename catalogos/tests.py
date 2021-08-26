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
        CatMotivosRechazo.objects.create(descripcion='no se que mas poner', tipo=2)
        CatMotivosRechazo.objects.create(descripcion='ganaron los steelers', tipo=1)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/catalogo/motivo-rechazo/list/steelers/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/catalogo/motivo-rechazo/list/poner/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/catalogo/motivo-rechazo/list/all/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostMotivoRechazoTest(APITestCase):
    def setUp(self):

        self.json = {
            "descripcion": "descricpcion 9",
            "tipo": 1,
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/catalogo/motivo-rechazo/create/', data=json.dumps(self.json), content_type="application/json")
        # print(f'response JSON ===>>> \n {json.dumps(response.data, cls=DecimalEncoder)} \n ---')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PutMotivoRechazoTest(APITestCase):
    def setUp(self):
        CatMotivosRechazo.objects.create(descripcion='muchos fallos', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='no sirve', tipo=2)
        CatMotivosRechazo.objects.create(descripcion='perdieron los steelers', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='engargolado incorrecto', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='documento perdido', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='no se que mas poner fall', tipo=2)
        CatMotivosRechazo.objects.create(descripcion='ganaron los steelers', tipo=1)

        self.json = {
            "descripcion": "descricpcion 9",
            "tipo": 2,
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put('/api/catalogo/motivo-rechazo/3/update/', data=json.dumps(self.json), content_type="application/json")
        # print(f'response JSON ===>>> \n {json.dumps(response.data, cls=DecimalEncoder)} \n ---')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteMotivoRechazoTest(APITestCase):
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

        cuenta = CatMotivosRechazo.objects.all().count()
        print(f'--->>>cuenta registros antes: {cuenta}')

        response = self.client.delete('/api/catalogo/motivo-rechazo/3/delete/')
        print(f'response JSON ===>>> ok 204 sin contenido \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        cuenta = CatMotivosRechazo.objects.all().count()
        print(f'--->>>cuenta registros despues: {cuenta}')


# usado para corregir error de que json.dumps no puede mostrar los tipos Decimal, aqui regreso un float
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            # return str(o)
            return float(o)
        return super(DecimalEncoder, self).default(o)


# class PostCatPagosTest(APITestCase):
#     def setUp(self):

#         self.json = {
#             "descripcion": "descricpcion 6",
#             "precio": 369.99,
#             "tipo": 6,
#         }

#         self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

#     def test(self):
#         self.client.force_authenticate(user=self.user)

#         response = self.client.post('/api/catalogo/pagos/create/', data=json.dumps(self.json), content_type="application/json")
#         # print(f'response JSON ===>>> \n {json.dumps(response.data, cls=DecimalEncoder)} \n ---')
#         print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class GetCatPagosFilteredListTest(APITestCase):
    def setUp(self):
        # CatPagos.objects.create(descripcion='descripcion1', tipo=5, precio=123.45)
        # CatPagos.objects.create(descripcion='descripcion2', tipo=4, precio=456.78)
        # CatPagos.objects.create(descripcion='descripcion3', tipo=6, precio=369.69)
        # CatPagos.objects.create(descripcion='descripcion4', tipo=3, precio=333.33)
        # CatPagos.objects.create(descripcion='descripcion5', tipo=1, precio=666.66)
        # CatPagos.objects.create(descripcion='descripcion6', tipo=3, precio=999.99)
        
        CatPagos.objects.create(descripcion='Examen Certificación Vigente', precio=123.45)
        CatPagos.objects.create(descripcion='Examen Convocatoria Nacional', precio=456.78)
        CatPagos.objects.create(descripcion='Examen Convocatoria Extranjero', precio=369.69)
        CatPagos.objects.create(descripcion='Examen Especial de Certificación', precio=333.33)
        CatPagos.objects.create(descripcion='Actividad Asistencial', precio=666.66)
        CatPagos.objects.create(descripcion='Renovación de Certificación', precio=999.99)

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/catalogo/pagos/list/?descripcionNS=nacional')
        print(f'response JSON ===>>> descripcionNS=descripcion1 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/catalogo/pagos/list/')
        print(f'response JSON ===>>> all ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class PutCatPagosTest(APITestCase):
    def setUp(self):
        # CatPagos.objects.create(descripcion='descripcion1', tipo=5, precio=123.45)
        # CatPagos.objects.create(descripcion='descripcion2', tipo=4, precio=456.78)
        # CatPagos.objects.create(descripcion='descripcion3', tipo=1, precio=111.11)
        # CatPagos.objects.create(descripcion='descripcion4', tipo=3, precio=333.33)
        # CatPagos.objects.create(descripcion='descripcion5', tipo=1, precio=666.66)
        # CatPagos.objects.create(descripcion='descripcion6', tipo=3, precio=999.99)
        
        CatPagos.objects.create(descripcion='Examen Certificación Vigente', precio=123.45)
        CatPagos.objects.create(descripcion='Examen Convocatoria Nacional', precio=456.78)
        CatPagos.objects.create(descripcion='Examen Convocatoria Extranjero', precio=369.69)
        CatPagos.objects.create(descripcion='Examen Especial de Certificación', precio=333.33)
        CatPagos.objects.create(descripcion='Actividad Asistencial', precio=666.66)
        CatPagos.objects.create(descripcion='Renovación de Certificación', precio=999.99)

        self.json = {
            "precio": 111.11
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/catalogo/pagos/list/?descripcionNS=extranjero')
        print(f'response JSON ===>>> descripcionNS=descripcion1 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put('/api/catalogo/pagos/3/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get('/api/catalogo/pagos/list/?descripcionNS=extranjero')
        print(f'response JSON ===>>> descripcionNS=descripcion1 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetCatEntidadListTest(APITestCase):
    def setUp(self):
        CatEntidad.objects.create(entidad = 'Entidad1', region = 'Region1')
        CatEntidad.objects.create(entidad = 'Entidad2', region = 'Region2')
        CatEntidad.objects.create(entidad = 'Entidad3', region = 'Region3')
        self.user = User.objects.create_user(username = 'billy', is_staff = True)
    def test(self):
        self.client.force_authenticate(user = self.user)
        response = self.client.get('/api/catalogo/entidad/list/')
        print(f'response JSON ===>>> 200-OK \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)