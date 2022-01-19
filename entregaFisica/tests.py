from django.test import TestCase
from .models import *
from datetime import date
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from dateutil.relativedelta import relativedelta


def configDB():
    ctde1 = CatTiposDocumentoEntrega.objects.create(descripcion='Certificado1')
    ctde2 = CatTiposDocumentoEntrega.objects.create(descripcion='Certificado2')
    ctde3 = CatTiposDocumentoEntrega.objects.create(descripcion='Certificado3')

    medico = Medico.objects.create(
        nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp3', fechaNac='2020-09-09', pais='pais3', estado='estado3', ciudad='ciudad3',
        deleMuni='deleMuni3', colonia='colonia', calle='calle3', cp='cp3', numExterior='numExterior3', rfcFacturacion='rfcFacturacion3', cedProfesional='cedProfesional3',
        cedEspecialidad='cedEspecialidad3', cedCirugiaGral='cedCirugiaGral3', hospitalResi='hospitalResi3', telJefEnse='telJefEnse3', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular3', telParticular='telParticular3', email='gabriel@mb.company', numRegistro=333, aceptado=True, telConsultorio='telConsultorio3', sexo='M',
        anioCertificacion=2022, isConsejero=True, isProfesor=False, isCertificado=False, estudioExtranjero=False, isExtranjero=False)
    medico2 = Medico.objects.create(
        nombre='elianid', apPaterno='tolentino', apMaterno='tolentino', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', email='elianid@mb.company', numRegistro=111, aceptado=True, telConsultorio='telConsultorio1', sexo='F',
        anioCertificacion=2022, isConsejero=True, isProfesor=False, isCertificado=True, estudioExtranjero=False, isExtranjero=False)

    EntregaFisica.objects.create(fechaEntrega=date.today(), catTiposDocumentoEntrega=ctde1, nombreRecibe='nombre de quien recibe1',
                                 libro=1, foja=1, archivo='ninguno1', comentarios='ninguno1', medico=medico)
    EntregaFisica.objects.create(fechaEntrega=date.today() + relativedelta(days=8), catTiposDocumentoEntrega=ctde2,
                                 nombreRecibe='nombre de quien recibe2', libro=2, foja=2, archivo='ninguno2', comentarios='ninguno2', medico=medico2)
    EntregaFisica.objects.create(fechaEntrega=date.today(), catTiposDocumentoEntrega=ctde2, nombreRecibe='nombre de quien recibe3',
                                 libro=3, foja=3, archivo='ninguno3', comentarios='ninguno3', medico=medico)
    EntregaFisica.objects.create(fechaEntrega=date.today() + relativedelta(days=8), catTiposDocumentoEntrega=ctde1,
                                 nombreRecibe='nombre de quien recibe4', libro=4, foja=4, archivo='ninguno4', comentarios='ninguno4', medico=medico2)
    EntregaFisica.objects.create(fechaEntrega=date.today(), catTiposDocumentoEntrega=ctde1, nombreRecibe='nombre de quien recibe5',
                                 libro=5, foja=5, archivo='ninguno5', comentarios='ninguno5', medico=medico)
    EntregaFisica.objects.create(fechaEntrega=date.today() + relativedelta(days=8), catTiposDocumentoEntrega=ctde2,
                                 nombreRecibe='nombre de quien recibe6', libro=6, foja=6, archivo='ninguno6', comentarios='ninguno6', medico=medico2)


# python manage.py test entregaFisica.tests.BaseDatosTest
class BaseDatosTest(APITestCase):
    def setUp(self):
        configDB()
        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        datos = EntregaFisica.objects.all()
        for dato in datos:
            print(f'--->>>id: {dato.id} - nombreRecibe: {dato.nombreRecibe} - fechaEntrega: {dato.fechaEntrega} - medico: {dato.medico}')


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
            "medico": 1
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


# python manage.py test entregaFisica.tests.GetEntregaFisicaFilteredListTest
class GetEntregaFisicaFilteredListTest(APITestCase):
    def setUp(self):

        configDB()

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/entrega-fisica/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/entrega-fisica/list/?nombreRecibeNS=recibe3')
        print(f'response JSON ===>>> nombreRecibeNS=recibe3 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        fecha = str(date.today())
        response = self.client.get('/api/entrega-fisica/list/?fechaEntrega='+fecha)
        print(f'response JSON ===>>> fechaEntrega={fecha} \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/entrega-fisica/list/?medico=1')
        print(f'response JSON ===>>> medico=1 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# python manage.py test entregaFisica.tests.GetEntregaFisicaDetailTest
class GetEntregaFisicaDetailTest(APITestCase):
    def setUp(self):

        configDB()

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/entrega-fisica/3/detail/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/entrega-fisica/33/detail/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# python manage.py test entregaFisica.tests.PutEntregaFisicaUpdateTest
class PutEntregaFisicaUpdateTest(APITestCase):
    def setUp(self):

        configDB()

        archivo = open('./uploads/testUnit.jpg', 'rb')
        archivoFile = SimpleUploadedFile(archivo.name, archivo.read(), content_type='image/jpg')

        self.json = {
            "fechaEntrega": "2222-02-02",
            "catTiposDocumentoEntrega": 2,
            "nombreRecibe": "Sutanita chiquita ",
            "libro": 9,
            "foja": 12,
            "archivo": archivoFile,
            "comentarios": "comentarios chidos modificados",
            "medico": 2
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put('/api/entrega-fisica/3/update/', data=self.json, format='multipart')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# python manage.py test entregaFisica.tests.DeleteEntregaFisicaTest
class DeleteEntregaFisicaTest(APITestCase):
    def setUp(self):

        configDB()

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.delete('/api/entrega-fisica/3/delete/')
        print(f'response JSON ===>>> ok 204 sin contenido \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.delete('/api/entrega-fisica/33/delete/')
        print(f'response JSON ===>>> ok 204 sin contenido \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# python manage.py test entregaFisica.tests.PostCatTiposDocumentoEntregaTest
class PostCatTiposDocumentoEntregaTest(APITestCase):
    def setUp(self):

        configDB()

        self.json = {
            "descripcion": "descripcion1",
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/entrega-fisica/tipo-documento/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> ok \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# python manage.py test entregaFisica.tests.GetCatTiposDocumentoEntregaListTest
class GetCatTiposDocumentoEntregaListTest(APITestCase):
    def setUp(self):

        configDB()

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/entrega-fisica/tipo-documento/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# python manage.py test entregaFisica.tests.GetCatTiposDocumentoEntregaDetailTest
class GetCatTiposDocumentoEntregaDetailTest(APITestCase):
    def setUp(self):

        configDB()

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/entrega-fisica/tipo-documento/3/detail/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# python manage.py test entregaFisica.tests.PutCatTiposDocumentoEntregaTest
class PutCatTiposDocumentoEntregaTest(APITestCase):
    def setUp(self):

        configDB()

        self.json = {
            "descripcion": "descripcionModificada",
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put('/api/entrega-fisica/tipo-documento/3/update/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> ok \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
