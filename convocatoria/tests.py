from convocatoria.models import Convocatoria
from preregistro.models import Medico
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from io import BytesIO, StringIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from .serializers import *
import json

from datetime import date

import requests

# Create your tests here.


class PutEsExtranjero200Test(APITestCase):
    def setUp(self):
        Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        self.json = {
            "isExtranjero": "False",
            "nacionalidad": "Indio"
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = Medico.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.nombre} - {dato.isExtranjero} - {dato.nacionalidad}')

        response = self.client.put('/api/convocatoria/medico/es-extranjero/1/', self.json)
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Medico.objects.get(id=1)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.nombre} - {dato.isExtranjero} - {dato.nacionalidad}')


class PutEstudioExtranjero200Test(APITestCase):
    def setUp(self):
        Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        self.json = {
            "estudioExtranjero": True,
            "escuelaExtranjero": "MIT"
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = Medico.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.nombre} - {dato.estudioExtranjero} - {dato.escuelaExtranjero}')

        response = self.client.put('/api/convocatoria/medico/estudio-extranjero/1/', self.json)
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Medico.objects.get(id=1)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.nombre} - {dato.estudioExtranjero} - {dato.escuelaExtranjero}')


class PostConvocatoria200Test(APITestCase):
    def setUp(self):
        CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')

        self.json = {
            "fechaInicio": "2020-06-04",
            "fechaTermino": "2021-02-11",
            "fechaExamen": "2021-04-06",
            "horaExamen": "09:09",
            "nombre": "convocatoria chingona",
            "detalles": "detalles",
            "precio": 369.99,
            "sedes": [
                {"catSedes": 1},
                {"catSedes": 2},
            ],
            "tiposExamen": [
                {"catTiposExamen": 1}
            ]
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/convocatoria/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        print(f'\n --->>> checando la DB <<<---')

        print(f'\n --->>>#registros convocatoria: {Convocatoria.objects.count()}')
        print(f'\n --->>>#registros sede: {Sede.objects.count()}')
        print(f'\n --->>>#registros tipoExamenes: {TipoExamen.objects.count()}')

        print(f'\n --->>>nombre: {Convocatoria.objects.get().nombre}')
        print(f'\n --->>>sede1: {Sede.objects.get(id=1).catSedes.descripcion}')
        print(f'\n --->>>sede2: {Sede.objects.get(id=2).catSedes.descripcion}')
        print(f'\n --->>>tipoExamen1: {TipoExamen.objects.get(id=1).catTiposExamen.descripcion}')


class GetList200Test(APITestCase):
    def setUp(self):
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1',
                                    precio=333.33)
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona2', detalles='detalles1',
                                    precio=333.33)
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-03-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona3', detalles='detalles1',
                                    precio=333.33)
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona4', detalles='detalles1',
                                    precio=333.33)
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona5', detalles='detalles1',
                                    precio=333.33)
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-03-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles1',
                                    precio=333.33)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/convocatoria/list/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # data = Convocatoria.objects.filter(fechaTermino__gte=date.today())
        # print(f'--->>>data: {data}')


class GetDetail200Test(APITestCase):
    def setUp(self):
        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        catSedes2 = CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
        catTiposExamen2 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')

        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1',
                                    precio=333.33)
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona2', detalles='detalles1',
                                    precio=333.33)
        self.convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-03-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona3',
                                                        detalles='detalles3', precio=333.33)
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona4', detalles='detalles1',
                                    precio=333.33)
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona5', detalles='detalles1',
                                    precio=333.33)
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-15', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles1',
                                    precio=333.33)

        Sede.objects.create(catSedes=catSedes1, convocatoria=self.convocatoria)
        Sede.objects.create(catSedes=catSedes3, convocatoria=self.convocatoria)

        TipoExamen.objects.create(catTiposExamen=catTiposExamen1, convocatoria=self.convocatoria)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/convocatoria/detail/3/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # serializer = ConvocatoriaGetDetailSerializer(instance=self.convocatoria)
        # print(serializer.data)

        # print(f'\n --->>>sede.count: {Sede.objects.count()} \n ---')
        # serializer = SedeSerializer(instance=Sede.objects.get(id=1))
        # print(serializer.data)


class PutArchivo200Test(APITestCase):
    def setUp(self):
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona', detalles='detalles',
                                    precio=369.99)

        streamPDF = BytesIO(
            b'%PDF-1.0\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1'
            b'>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 3 3]>>endobj\nxref\n0 4\n0000000000 65535 f\n000000'
            b'0010 00000 n\n0000000053 00000 n\n0000000102 00000 n\ntrailer<</Size 4/Root 1 0 R>>\nstartxre'
            b'f\n149\n%EOF\n')

        pdfFile = SimpleUploadedFile('./uploads/convocatoria.pdf', streamPDF.read(), content_type='application/pdf')

        self.json = {
            "archivo": pdfFile
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = Convocatoria.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.nombre} - {dato.archivo}')

        response = self.client.put('/api/convocatoria/1/archivo/', data=self.json, format='multipart')
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Convocatoria.objects.get(id=1)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.nombre} - {dato.archivo}')


class PutBanner200Test(APITestCase):
    def setUp(self):
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona', detalles='detalles',
                                    precio=369.99)

        stream = BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(stream, format='jpeg')

        pngFile = SimpleUploadedFile('./uploads/banner.png', stream.getvalue(), content_type='image/png')

        self.json = {
            "banner": pngFile
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = Convocatoria.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.nombre} - {dato.banner}')

        response = self.client.put('/api/convocatoria/1/banner/', data=self.json, format='multipart')
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Convocatoria.objects.get(id=1)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.nombre} - {dato.banner}')


class PostEnrolar200Test(APITestCase):
    def setUp(self):
        CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')

        Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1',
                                    precio=333.33)

        self.json = {
            "medico": 1,
            "convocatoria": 1,
            "catTiposExamen": 1,
            "catSedes": 1,
            "isPagado": False,
            "comentario": "por que quiero",
            "isAceptado": True
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/convocatoria/enrolar/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        dato = ConvocatoriaEnrolado.objects.get(id=1)
        print(f'--->>>dato: {dato.id} - {dato.isPagado} - {dato.comentario} - {dato.isAceptado}')


class PostDocumento200Test(APITestCase):
    def setUp(self):
        CatTiposDocumento.objects.create(descripcion='Revalidación')
        CatTiposDocumento.objects.create(descripcion='CURP')
        CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')
        
        

        CatMotivosRechazo.objects.create(descripcion='descripcion1', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='descripcion2', tipo=2)

        Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1',
                                    precio=333.33)

        stream = BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(stream, format='jpeg')

        pngFile = SimpleUploadedFile('./uploads/banner.png', stream.getvalue(), content_type='image/png')

        self.json = {
            "medico": 1,
            "convocatoria": 1,
            "catTiposDocumento": 6,
            "documento": pngFile,
            "isValidado": True,
            "engargoladoOk": True,
            "notasValidado": "notas de validacion",
            "notasEngargolado": "notas de engargolado",
            "rechazoValidado": "motivo de rechazo en validacion",
            "rechazoEngargolado": "motivo de rechazo de engargolado"
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # response = self.client.post('/api/convocatoria/documento/revalidacion/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # self.json['catTiposDocumento'] = 999999

        # response = self.client.post('/api/convocatoria/documento/curp/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # response = self.client.post('/api/convocatoria/documento/acta-nacimiento/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # response = self.client.post('/api/convocatoria/documento/carta-solicitud/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # response = self.client.post('/api/convocatoria/documento/constancia-posgrado/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # response = self.client.post('/api/convocatoria/documento/cedula-especialidad/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # response = self.client.post('/api/convocatoria/documento/titulo-licenciatura/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # response = self.client.post('/api/convocatoria/documento/cedula-profesional/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # response = self.client.post('/api/convocatoria/documento/constancia-cirugia/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response = self.client.post('/api/convocatoria/documento/carta-profesor/create/', data=self.json, format='multipart')
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        dato = ConvocatoriaEnroladoDocumento.objects.get(id=1)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.isValidado} - {dato.notasEngargolado} - {dato.catTiposDocumento.descripcion}')


class baseDatosTest(APITestCase):
    def setUp(self):
        convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09',
                                                   nombre='convocatoria chingona', archivo='pdfFile', banner='pngFile', detalles='detalles', precio=369.99)

    def test(self):
        datoConvocatoria = Convocatoria.objects.get(id=1)
        print(f'--->>>dato: {datoConvocatoria}')
        serializer = ConvocatoriaSerializer(data=datoConvocatoria)
        print(f'--->>>serializer: {serializer}')
        if serializer.is_valid():
            # print(f'--->>>dato: {serializer.data}')
            print(set(serializer.data.keys()))
        print(f'--->>>dato: {serializer.errors}')
