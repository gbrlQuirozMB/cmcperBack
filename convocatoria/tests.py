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

from notificaciones.models import Notificacion


# Create your tests here.


class PutEsExtranjero200Test(APITestCase):
    def setUp(self):
        Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        self.json = {
            "isExtranjero": "True",
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
            "sedes": [
                {"catSedes": 1},
                {"catSedes": 2}
            ],
            "tiposExamen": [
                {"catTiposExamen": 1}
            ],
            "fechaResolucion": "2021-06-06"
        }
        #  campos incorrectos: {'sedes': [{}, {'catSedes': [ErrorDetail(string='Tipo incorrecto. Se esperaba valor de clave primaria y se recibió str.', code='incorrect_type')]}]}

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # print(json.dumps(self.json))
        # print(self.json)
        response = self.client.post('/api/convocatoria/create/', data=json.dumps(self.json), content_type="application/json")
        # response = self.client.post('/api/convocatoria/create/', data=self.json)
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
        print(f'\n --->>>fechaResolucion: {Convocatoria.objects.get().fechaResolucion}')


class GetList200Test(APITestCase):
    def setUp(self):
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1',
                                    )
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona2', detalles='detalles1',
                                    )
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-03-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona3', detalles='detalles1',
                                    )
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona4', detalles='detalles1',
                                    )
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona5', detalles='detalles1',
                                    )
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-03-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles1',
                                    )

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
                                    )
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona2', detalles='detalles1',
                                    )
        self.convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-03-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona3',
                                                        detalles='detalles3', archivo='archivo.pdf', banner='banner.jpg')
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona4', detalles='detalles1',
                                    )
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona5', detalles='detalles1',
                                    )
        Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-15', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles1',
                                    )

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
                                    )

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
                                    )

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


class PutConvocatoria200Test(APITestCase):
    def setUp(self):
        catSedes = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')

        convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                   horaExamen='09:09', nombre='convocatoria chingona', detalles='detalles', )

        Sede.objects.create(catSedes=catSedes, convocatoria=convocatoria)
        TipoExamen.objects.create(catTiposExamen=catTiposExamen, convocatoria=convocatoria)

        self.json = {
            "fechaInicio": "1999-06-04",
            "fechaTermino": "1999-02-11",
            "fechaExamen": "1999-04-06",
            "horaExamen": "03:03",
            "nombre": "convocatoria chingona modificada",
            "detalles": "detalles modificados",
            "sedes": [
                {"catSedes": 2},
                {"catSedes": 3},
            ],
            "tiposExamen": [
                {"catTiposExamen": 2}
            ]
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/convocatoria/detail/1/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Convocatoria.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.nombre} - {dato.fechaInicio}')

        response = self.client.put('/api/convocatoria/update/1/', data=json.dumps(self.json), content_type="application/json")
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Convocatoria.objects.get(id=1)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.nombre} - {dato.fechaInicio}')

        response = self.client.get('/api/convocatoria/detail/1/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteConvocatoria200Test(APITestCase):
    def setUp(self):
        catSedes = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')

        convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                   horaExamen='09:09', nombre='convocatoria chingona', detalles='detalles', )

        Sede.objects.create(catSedes=catSedes, convocatoria=convocatoria)
        TipoExamen.objects.create(catTiposExamen=catTiposExamen, convocatoria=convocatoria)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/convocatoria/detail/1/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete('/api/convocatoria/delete/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/api/convocatoria/detail/1/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        print(f'\n --->>> checando la DB <<<---')

        print(f'\n --->>>#registros convocatoria: {Convocatoria.objects.count()}')
        print(f'\n --->>>#registros sede: {Sede.objects.count()}')
        print(f'\n --->>>#registros tipoExamenes: {TipoExamen.objects.count()}')


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
                                    )

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

        response = self.client.post('/api/convocatoria/enrolar/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class PostDocumento200Test(APITestCase):
    def setUp(self):
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

        catTiposDocumento1 = CatTiposDocumento.objects.create(descripcion='Revalidación')
        catTiposDocumento2 = CatTiposDocumento.objects.create(descripcion='CURP')
        catTiposDocumento3 = CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        catTiposDocumento4 = CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        catTiposDocumento5 = CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        catTiposDocumento6 = CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        catTiposDocumento7 = CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        catTiposDocumento8 = CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        catTiposDocumento9 = CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        catTiposDocumento10 = CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')
        catTiposDocumento11 = CatTiposDocumento.objects.create(descripcion='Ficha de Registro')
        catTiposDocumento12 = CatTiposDocumento.objects.create(descripcion='Fotografía')

        CatMotivosRechazo.objects.create(descripcion='descripcion1', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='descripcion2', tipo=2)

        medico = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                   horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')

        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento1, documento='revalidacion.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento2, documento='curp.pdf', isValidado=True)
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento3, documento='acta_nacimiento.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento4, documento='carta_solicitud_examen.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento5, documento='constancia_posgrago.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento6, documento='cedula_especialidad.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento7, documento='titulo_licenciatura.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento8, documento='cedula_profesional.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento9, documento='constancia_cirugia.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento10, documento='carta_profesor.pdf', isValidado=False,
                                                     notasValidado='me cae gordo', rechazoValidado='carta incorrecta')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento12, documento='fotografia.jpg')
        

        stream = BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(stream, format='jpeg')

        pngFile = SimpleUploadedFile('./uploads/banner.png', stream.getvalue(), content_type='image/png')

        self.json = {
            "medico": 1,
            "convocatoria": 1,
            # "catTiposDocumento": 6,
            "documento": pngFile
            # "isValidado": True,
            # "engargoladoOk": True,
            # "notasValidado": "notas de validacion",
            # "notasEngargolado": "notas de engargolado",
            # "rechazoValidado": "motivo de rechazo en validacion",
            # "rechazoEngargolado": "motivo de rechazo de engargolado"
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=1).count()
        # print(f'--->>>cuenta: {cuenta}')
        # response = self.client.post('/api/convocatoria/documento/revalidacion/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=1).count()
        # print(f'--->>>cuenta: {cuenta}')

        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=2).count()
        # print(f'--->>>cuenta: {cuenta}')
        # response = self.client.post('/api/convocatoria/documento/curp/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=2).count()
        # print(f'--->>>cuenta: {cuenta}')

        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=3).count()
        # print(f'--->>>cuenta: {cuenta}')
        # response = self.client.post('/api/convocatoria/documento/acta-nacimiento/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=3).count()
        # print(f'--->>>cuenta: {cuenta}')

        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=4).count()
        # print(f'--->>>cuenta: {cuenta}')
        # response = self.client.post('/api/convocatoria/documento/carta-solicitud/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=4).count()
        # print(f'--->>>cuenta: {cuenta}')

        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=5).count()
        # print(f'--->>>cuenta: {cuenta}')
        # response = self.client.post('/api/convocatoria/documento/constancia-posgrado/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=5).count()
        # print(f'--->>>cuenta: {cuenta}')

        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=6).count()
        # print(f'--->>>cuenta: {cuenta}')
        # response = self.client.post('/api/convocatoria/documento/cedula-especialidad/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=6).count()
        # print(f'--->>>cuenta: {cuenta}')

        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=7).count()
        # print(f'--->>>cuenta: {cuenta}')
        # response = self.client.post('/api/convocatoria/documento/titulo-licenciatura/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=7).count()
        # print(f'--->>>cuenta: {cuenta}')

        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=8).count()
        # print(f'--->>>cuenta: {cuenta}')
        # response = self.client.post('/api/convocatoria/documento/cedula-profesional/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=8).count()
        # print(f'--->>>cuenta: {cuenta}')

        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=9).count()
        # print(f'--->>>cuenta: {cuenta}')
        # response = self.client.post('/api/convocatoria/documento/constancia-cirugia/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=9).count()
        # print(f'--->>>cuenta: {cuenta}')

        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=10).count()
        # print(f'--->>>cuenta: {cuenta}')
        # response = self.client.post('/api/convocatoria/documento/carta-profesor/create/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=10).count()
        # print(f'--->>>cuenta: {cuenta}')
        
        
        cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=12).count()
        print(f'--->>>cuenta: {cuenta}')
        response = self.client.post('/api/convocatoria/documento/foto/create/', data=self.json, format='multipart')
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cuenta = ConvocatoriaEnroladoDocumento.objects.filter(catTiposDocumento__id=12).count()
        print(f'--->>>cuenta: {cuenta}')
        
        
        # dato = ConvocatoriaEnroladoDocumento.objects.get(id=11)
        # print(f'--->>>DESPUES dato: {dato.id} - {dato.isValidado} - {dato.notasEngargolado} - {dato.catTiposDocumento.descripcion}')

        cuenta = Notificacion.objects.count()
        if cuenta != 0:
            dato = Notificacion.objects.get(id=1)
            print(f'--->>>dato: titulo: {dato.titulo}, mensaje: {dato.mensaje}, destinatario: {dato.destinatario}, remitente: {dato.remitente}')


class GetDocumentosList200Test(APITestCase):
    def setUp(self):
        catTiposDocumento1 = CatTiposDocumento.objects.create(descripcion='Revalidación')
        catTiposDocumento2 = CatTiposDocumento.objects.create(descripcion='CURP')
        catTiposDocumento3 = CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        catTiposDocumento4 = CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        catTiposDocumento5 = CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        catTiposDocumento6 = CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        catTiposDocumento7 = CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        catTiposDocumento8 = CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        catTiposDocumento9 = CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        catTiposDocumento10 = CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')
        catTiposDocumento11 = CatTiposDocumento.objects.create(descripcion='Ficha de Registro')
        catTiposDocumento12 = CatTiposDocumento.objects.create(descripcion='Fotografía')


        CatMotivosRechazo.objects.create(descripcion='descripcion1', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='descripcion2', tipo=2)

        medico = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                   horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1', )

        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento1, documento='revalidacion.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento2, documento='curp.pdf', isValidado=True)
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento3, documento='acta_nacimiento.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento4, documento='carta_solicitud_examen.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento5, documento='constancia_posgrago.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento6, documento='cedula_especialidad.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento7, documento='titulo_licenciatura.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento8, documento='cedula_profesional.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento9, documento='constancia_cirugia.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento10, documento='carta_profesor.pdf', isValidado=True,
                                                     notasValidado='me cae gordo', rechazoValidado='carta incorrecta')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento11, documento='ficha_registro.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento12, documento='foto.jpg')
        

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # response = self.client.get('/api/convocatoria/documentos/medico/1/list/')
        response = self.client.get('/api/convocatoria/1/medico/1/documentos/list/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        cuenta = ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, isValidado=True).count()
        print(f'--->>>cuenta: {cuenta}')

        # dato = ConvocatoriaEnroladoDocumento.objects.filter(medico=1)


class PutDocumento200Test(APITestCase):
    def setUp(self):
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

        catTiposDocumento1 = CatTiposDocumento.objects.create(descripcion='Revalidación')
        catTiposDocumento2 = CatTiposDocumento.objects.create(descripcion='CURP')
        catTiposDocumento3 = CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        catTiposDocumento4 = CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        catTiposDocumento5 = CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        catTiposDocumento6 = CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        catTiposDocumento7 = CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        catTiposDocumento8 = CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        catTiposDocumento9 = CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        catTiposDocumento10 = CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')
        catTiposDocumento11 = CatTiposDocumento.objects.create(descripcion='Ficha de Registro')
        catTiposDocumento12 = CatTiposDocumento.objects.create(descripcion='Fotografía')

        CatMotivosRechazo.objects.create(descripcion='descripcion1', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='descripcion2', tipo=2)

        medico = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                   horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1', )

        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento1, documento='revalidacion.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento2, documento='curp.pdf', isValidado=True)
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento3, documento='acta_nacimiento.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento4, documento='carta_solicitud_examen.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento5, documento='constancia_posgrago.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento6, documento='cedula_especialidad.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento7, documento='titulo_licenciatura.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento8, documento='cedula_profesional.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento9, documento='constancia_cirugia.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento10, documento='carta_profesor.pdf', isValidado=False,
                                                     notasValidado='me cae gordo', rechazoValidado='carta incorrecta')

        stream = BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(stream, format='jpeg')

        pngFile = SimpleUploadedFile('./uploads/banner.png', stream.getvalue(), content_type='image/png')

        self.json = {
            "documento": pngFile
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = ConvocatoriaEnroladoDocumento.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.documento}')

        response = self.client.put('/api/convocatoria/documento/update/1/', data=self.json, format='multipart')
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = ConvocatoriaEnroladoDocumento.objects.get(id=1)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.documento}')

        cuenta = Notificacion.objects.count()
        if cuenta != 0:
            dato = Notificacion.objects.get(id=1)
            print(f'--->>>dato: titulo: {dato.titulo}, mensaje: {dato.mensaje}, destinatario: {dato.destinatario}, remitente: {dato.remitente}')


class GetMedicoEnroladoDetails200Test(APITestCase):
    def setUp(self):
        CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')

        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles6')

        ConvocatoriaEnrolado.objects.create(id=99, medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen1)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/convocatoria/enrolar/medico/9/detail/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetMedicoEnroladoList200Test(APITestCase):
    def setUp(self):
        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion3')

        medico1 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico2 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico3 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')

        ConvocatoriaEnrolado.objects.create(medico=medico1, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1,)
        ConvocatoriaEnrolado.objects.create(medico=medico2, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/convocatoria/6/enrolados/false/all/all/list/')  # regresa TODOS
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        Medico.objects.filter(id=3).update(nombre='gabriel')
        response = self.client.get('/api/convocatoria/6/enrolados/false/GabRiel/all/list/')  # regresa gabriel quiroz y gabriel tolentino
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        Medico.objects.filter(id=3).update(nombre='laura', apPaterno='olvera')
        Medico.objects.filter(id=9).update(apPaterno='olvera')
        response = self.client.get('/api/convocatoria/6/enrolados/false/all/olVera/list/')  # regresa laura olvera y gabriel olvera
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        Medico.objects.filter(id=9).update(nombre='gabriel', apPaterno='quiroz')
        response = self.client.get('/api/convocatoria/6/enrolados/false/GABRIEL/Quiroz/list/')  # regresa laura olvera y gabriel olvera
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutEnroladoComentario200Test(APITestCase):
    def setUp(self):
        CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion3')

        medico3 = Medico.objects.create(
            id=3, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')

        ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3,)

        self.json = {
            "comentario": "Este es el comentario modificado"
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = ConvocatoriaEnrolado.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.comentario}')

        response = self.client.put('/api/convocatoria/enrolar/comentario/update/1/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = ConvocatoriaEnrolado.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.comentario}')


class PutDocumentoAceptar200Test(APITestCase):
    def setUp(self):
        catTiposDocumento1 = CatTiposDocumento.objects.create(descripcion='Revalidación')
        catTiposDocumento2 = CatTiposDocumento.objects.create(descripcion='CURP')
        catTiposDocumento3 = CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        catTiposDocumento4 = CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        catTiposDocumento5 = CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        catTiposDocumento6 = CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        catTiposDocumento7 = CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        catTiposDocumento8 = CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        catTiposDocumento9 = CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        catTiposDocumento10 = CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')

        CatMotivosRechazo.objects.create(descripcion='descripcion1', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='descripcion2', tipo=2)

        medico = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                   horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1', )

        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento1, documento='revalidacion.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento2, documento='curp.pdf', isValidado=True)
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento3, documento='acta_nacimiento.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento4, documento='carta_solicitud_examen.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento5, documento='constancia_posgrago.pdf')
        # ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento6, documento='cedula_especialidad.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento7, documento='titulo_licenciatura.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento8, documento='cedula_profesional.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento9, documento='constancia_cirugia.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento10, documento='carta_profesor.pdf', isValidado=False,
                                                     notasValidado='me cae gordo', rechazoValidado='carta incorrecta')

        self.json = {
            "isValidado": False
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated - IsAdminUser

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = ConvocatoriaEnroladoDocumento.objects.get(id=9)
        print(f'--->>>ANTES dato: {dato.id} - {dato.isValidado} - {dato.notasValidado} - {dato.rechazoValidado}')

        response = self.client.put('/api/convocatoria/documento/aceptar/9/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = ConvocatoriaEnroladoDocumento.objects.get(id=9)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.isValidado} - {dato.notasValidado} - {dato.rechazoValidado}')

        # response = self.client.get('/api/convocatoria/1/medico/1/documentos/list/')
        # print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutDocumentoRechazar200Test(APITestCase):
    def setUp(self):
        catTiposDocumento1 = CatTiposDocumento.objects.create(descripcion='Revalidación')
        catTiposDocumento2 = CatTiposDocumento.objects.create(descripcion='CURP')
        catTiposDocumento3 = CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        catTiposDocumento4 = CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        catTiposDocumento5 = CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        catTiposDocumento6 = CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        catTiposDocumento7 = CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        catTiposDocumento8 = CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        catTiposDocumento9 = CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        catTiposDocumento10 = CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')

        CatMotivosRechazo.objects.create(descripcion='descripcion1', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='descripcion2', tipo=2)

        medico = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                   horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1', )

        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento1, documento='revalidacion.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento2, documento='curp.pdf', isValidado=True)
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento3, documento='acta_nacimiento.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento4, documento='carta_solicitud_examen.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento5, documento='constancia_posgrago.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento6, documento='cedula_especialidad.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento7, documento='titulo_licenciatura.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento8, documento='cedula_profesional.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento9, documento='constancia_cirugia.pdf', isValidado=True)
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento10, documento='carta_profesor.pdf', isValidado=False,
                                                     notasValidado='me cae gordo', rechazoValidado='carta incorrecta')

        self.json = {
            "isValidado": True,
            "notasValidado": "esta mal esta chingadera",
            "rechazoValidado": "de un catalogo es la descripcion"
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated - IsAdminUser

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = ConvocatoriaEnroladoDocumento.objects.get(id=9)
        print(f'--->>>ANTES dato: {dato.id} - {dato.isValidado}')

        response = self.client.put('/api/convocatoria/documento/rechazar/9/', data=json.dumps(self.json), content_type="application/json")
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = ConvocatoriaEnroladoDocumento.objects.get(id=9)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.isValidado}')

        # response = self.client.get('/api/convocatoria/1/medico/1/documentos/list/')
        # print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutEngargoladoAceptar200Test(APITestCase):
    def setUp(self):
        catTiposDocumento1 = CatTiposDocumento.objects.create(descripcion='Revalidación')
        catTiposDocumento2 = CatTiposDocumento.objects.create(descripcion='CURP')
        catTiposDocumento3 = CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        catTiposDocumento4 = CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        catTiposDocumento5 = CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        catTiposDocumento6 = CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        catTiposDocumento7 = CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        catTiposDocumento8 = CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        catTiposDocumento9 = CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        catTiposDocumento10 = CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')

        CatMotivosRechazo.objects.create(descripcion='descripcion1', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='descripcion2', tipo=2)

        medico = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                   horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1', )

        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento1, documento='revalidacion.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento2, documento='curp.pdf', isValidado=True)
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento3, documento='acta_nacimiento.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento4, documento='carta_solicitud_examen.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento5, documento='constancia_posgrago.pdf')
        # ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento6, documento='cedula_especialidad.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento7, documento='titulo_licenciatura.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento8, documento='cedula_profesional.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento9, documento='constancia_cirugia.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento10, documento='carta_profesor.pdf', isValidado=False,
                                                     notasEngargolado='me cae gordo', rechazoEngargolado='carta incorrecta')

        self.json = {
            "engargoladoOk": False
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated - IsAdminUser

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = ConvocatoriaEnroladoDocumento.objects.get(id=9)
        print(f'--->>>ANTES dato: {dato.id} - {dato.isValidado} - {dato.notasEngargolado} - {dato.rechazoEngargolado}')

        response = self.client.put('/api/convocatoria/engargolado/aceptar/9/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = ConvocatoriaEnroladoDocumento.objects.get(id=9)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.isValidado} - {dato.notasEngargolado} - {dato.rechazoEngargolado}')

        # response = self.client.get('/api/convocatoria/1/medico/1/documentos/list/')
        # print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutEngargoladoRechazar200Test(APITestCase):
    def setUp(self):
        catTiposDocumento1 = CatTiposDocumento.objects.create(descripcion='Revalidación')
        catTiposDocumento2 = CatTiposDocumento.objects.create(descripcion='CURP')
        catTiposDocumento3 = CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        catTiposDocumento4 = CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        catTiposDocumento5 = CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        catTiposDocumento6 = CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        catTiposDocumento7 = CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        catTiposDocumento8 = CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        catTiposDocumento9 = CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        catTiposDocumento10 = CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')

        CatMotivosRechazo.objects.create(descripcion='descripcion1', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='descripcion2', tipo=2)

        medico = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                   horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1', )

        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento1, documento='revalidacion.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento2, documento='curp.pdf', isValidado=True)
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento3, documento='acta_nacimiento.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento4, documento='carta_solicitud_examen.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento5, documento='constancia_posgrago.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento6, documento='cedula_especialidad.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento7, documento='titulo_licenciatura.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento8, documento='cedula_profesional.pdf')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento9, documento='constancia_cirugia.pdf', isValidado=True)
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento10, documento='carta_profesor.pdf', isValidado=False,
                                                     notasValidado='me cae gordo', rechazoValidado='carta incorrecta')

        self.json = {
            "engargoladoOk": True,
            "notasEngargolado": "esta mal esta chingadera",
            "rechazoEngargolado": "de un catalogo es la descripcion"
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated - IsAdminUser

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = ConvocatoriaEnroladoDocumento.objects.get(id=9)
        print(f'--->>>ANTES dato: {dato.id} - {dato.isValidado}')

        response = self.client.put('/api/convocatoria/engargolado/rechazar/9/', data=json.dumps(self.json), content_type="application/json")
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = ConvocatoriaEnroladoDocumento.objects.get(id=9)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.isValidado}')

        # response = self.client.get('/api/convocatoria/1/medico/1/documentos/list/')
        # print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetCostoAPagar200Test(APITestCase):
    def setUp(self):
        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(id=1, descripcion='tiposExameneDescripcion1', precio=111.11, precioExtrangero=222.22)
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(id=3, descripcion='tiposExameneDescripcion3', precio=333.33, precioExtrangero=444.44)

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles6')

        ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico6, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3, isAceptado=True)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # Si puede pagar
        response = self.client.get('/api/convocatoria/6/medico/9/a-pagar/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # no puede pagar
        ConvocatoriaEnrolado.objects.filter(id=3).update(isAceptado=False)
        response = self.client.get('/api/convocatoria/6/medico/9/a-pagar/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # no se encuentra el registro
        response = self.client.get('/api/convocatoria/6/medico/2/a-pagar/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PutPagado200Test(APITestCase):
    def setUp(self):
        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(id=1, descripcion='tiposExameneDescripcion1', precio=111.11, precioExtrangero=222.22)
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(id=3, descripcion='tiposExameneDescripcion3', precio=333.33, precioExtrangero=444.44)

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles6')

        ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico6, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3, isAceptado=True)

        # self.json = {
        #     "medicoId": 9,
        #     "convocatoriaId": 6
        # }

        # self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated - IsAdminUser
        self.user = User.objects.create_user(username='gabriel', is_staff=False)  # IsAuthenticated - IsAdminUser

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = ConvocatoriaEnrolado.objects.get(id=3)
        print(f'--->>>ANTES dato: {dato.id} - {dato.isPagado}')

        response = self.client.put('/api/convocatoria/enrolar/3/pagado/')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = ConvocatoriaEnrolado.objects.get(id=3)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.isPagado}')

        # no puede pagar
        ConvocatoriaEnrolado.objects.filter(id=3).update(isAceptado=False)
        # response = self.client.put('/api/convocatoria/enrolar/3/pagado/', data=json.dumps(self.json), content_type="application/json")
        response = self.client.put('/api/convocatoria/enrolar/3/pagado/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        # no se encuentra el registro
        # response = self.client.put('/api/convocatoria/enrolar/4/pagado/', data=json.dumps(self.json), content_type="application/json")
        response = self.client.put('/api/convocatoria/enrolar/4/pagado/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetEnviarCorreoEngargolado200Test(APITestCase):
    def setUp(self):
        catTiposDocumento1 = CatTiposDocumento.objects.create(descripcion='Revalidación')
        catTiposDocumento2 = CatTiposDocumento.objects.create(descripcion='CURP')
        catTiposDocumento3 = CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        catTiposDocumento4 = CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        catTiposDocumento5 = CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        catTiposDocumento6 = CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        catTiposDocumento7 = CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        catTiposDocumento8 = CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        catTiposDocumento9 = CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        catTiposDocumento10 = CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')
        catTiposDocumento11 = CatTiposDocumento.objects.create(descripcion='Ficha de Registro')

        CatMotivosRechazo.objects.create(descripcion='descripcion1', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='descripcion2', tipo=2)

        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)
        catTiposExamen1 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')

        medico = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                   horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1', )

        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento1,
                                                     documento='revalidacion.pdf', engargoladoOk=True, notasEngargolado='rev-NE', rechazoEngargolado='rev-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento2,
                                                     documento='curp.pdf', engargoladoOk=True, notasEngargolado='curp-NE', rechazoEngargolado='curp-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento3,
                                                     documento='acta_nacimiento.pdf', engargoladoOk=True, notasEngargolado='actN-NE', rechazoEngargolado='actN-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento4,
                                                     documento='carta_solicitud_examen.pdf', engargoladoOk=True, notasEngargolado='carS-NE', rechazoEngargolado='carS-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento5,
                                                     documento='constancia_posgrago.pdf', engargoladoOk=True, notasEngargolado='conP-NE', rechazoEngargolado='conP-RE')
        # ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento6,
        #                                              documento='cedula_especialidad.pdf', engargoladoOk=True, notasEngargolado='cedE-NE', rechazoEngargolado='cedE-RE') # YA NO SE UTILIZA EN ESTA HISTORIA
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento7,
                                                     documento='titulo_licenciatura.pdf', engargoladoOk=True, notasEngargolado='titL-NE', rechazoEngargolado='titL-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento8,
                                                     documento='cedula_profesional.pdf', engargoladoOk=True, notasEngargolado='cedP-NE', rechazoEngargolado='cedP-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento9,
                                                     documento='constancia_cirugia.pdf', engargoladoOk=True, notasEngargolado='conC-NE', rechazoEngargolado='conC-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento10,
                                                     documento='carta_profesor.pdf', engargoladoOk=True, notasEngargolado='carP-NE', rechazoEngargolado='carP-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento11,
                                                     documento='ficha_registro.pdf', engargoladoOk=True, notasEngargolado='fichR-NE', rechazoEngargolado='fichR-RE')

        ConvocatoriaEnrolado.objects.create(id=99, medico=medico, convocatoria=convocatoria, catSedes=catSedes3, catTiposExamen=catTiposExamen1)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # 10 documentos porque estudio en el extranjero y agrega ficha de registro envia correo de OK
        response = self.client.get('/api/convocatoria/1/medico/1/correo-engargolado/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dato = ConvocatoriaEnrolado.objects.get(medico=1, convocatoria=1)
        print(f'--->>>isAceptado: {dato.isAceptado}')

        # menos de  10 documentos porque estudio en el extranjero envia correo faltantes
        ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, catTiposDocumento=9).update(engargoladoOk=False)
        ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, catTiposDocumento=6).update(engargoladoOk=False)
        response = self.client.get('/api/convocatoria/1/medico/1/correo-engargolado/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dato = ConvocatoriaEnrolado.objects.get(medico=1, convocatoria=1)
        print(f'--->>>isAceptado: {dato.isAceptado}')

        # 9 documentos porque  es nacional envia correo de OK
        ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, catTiposDocumento=9).update(engargoladoOk=True)
        ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, catTiposDocumento=6).update(engargoladoOk=True)
        ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, catTiposDocumento=1).delete()
        Medico.objects.filter(id=1).update(estudioExtranjero=False)
        response = self.client.get('/api/convocatoria/1/medico/1/correo-engargolado/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dato = ConvocatoriaEnrolado.objects.get(medico=1, convocatoria=1)
        print(f'--->>>isAceptado: {dato.isAceptado}')

        # menos de 9 documentos porque  es nacional envia correo faltantes
        ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, catTiposDocumento=9).update(engargoladoOk=False)
        ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, catTiposDocumento=6).update(engargoladoOk=False)
        response = self.client.get('/api/convocatoria/1/medico/1/correo-engargolado/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dato = ConvocatoriaEnrolado.objects.get(medico=1, convocatoria=1)
        print(f'--->>>isAceptado: {dato.isAceptado}')

        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(medico=1,convocatoria=1,isValidado=True).count()
        # print(f'--->>>cuenta: {cuenta}')


class GetEnviarCorreoDocumentos200Test(APITestCase):
    def setUp(self):
        catTiposDocumento1 = CatTiposDocumento.objects.create(descripcion='Revalidación')
        catTiposDocumento2 = CatTiposDocumento.objects.create(descripcion='CURP')
        catTiposDocumento3 = CatTiposDocumento.objects.create(descripcion='Acta de Nacimiento')
        catTiposDocumento4 = CatTiposDocumento.objects.create(descripcion='Carta de Solicitud de Examen')
        catTiposDocumento5 = CatTiposDocumento.objects.create(descripcion='Constancia de Posgrado')
        catTiposDocumento6 = CatTiposDocumento.objects.create(descripcion='Cédula de Especialidad')
        catTiposDocumento7 = CatTiposDocumento.objects.create(descripcion='Título de la Licenciatura')
        catTiposDocumento8 = CatTiposDocumento.objects.create(descripcion='Cédula Profesional')
        catTiposDocumento9 = CatTiposDocumento.objects.create(descripcion='Constancia de Cirugía General')
        catTiposDocumento10 = CatTiposDocumento.objects.create(descripcion='Carta de Profesor Titular')
        catTiposDocumento11 = CatTiposDocumento.objects.create(descripcion='Ficha de Registro')
        catTiposDocumento12 = CatTiposDocumento.objects.create(descripcion='Fotografía')

        CatMotivosRechazo.objects.create(descripcion='descripcion1', tipo=1)
        CatMotivosRechazo.objects.create(descripcion='descripcion2', tipo=2)

        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)
        catTiposExamen1 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')

        medico = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                   horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1', )

        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento1,
                                                     documento='revalidacion.pdf', isValidado=True, notasValidado='rev-NE', rechazoValidado='rev-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento2,
                                                     documento='curp.pdf', isValidado=True, notasValidado='curp-NE', rechazoValidado='curp-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento3,
                                                     documento='acta_nacimiento.pdf', isValidado=True, notasValidado='actN-NE', rechazoValidado='actN-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento4,
                                                     documento='carta_solicitud_examen.pdf', isValidado=True, notasValidado='carS-NE', rechazoValidado='carS-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento5,
                                                     documento='constancia_posgrago.pdf', isValidado=True, notasValidado='conP-NE', rechazoValidado='conP-RE')
        # ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento6,
        #                                              documento='cedula_especialidad.pdf', isValidado=True, notasValidado='cedE-NE', rechazoValidado='cedE-RE') # YA NO SE UTILIZA EN ESTA HISTORIA
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento7,
                                                     documento='titulo_licenciatura.pdf', isValidado=True, notasValidado='titL-NE', rechazoValidado='titL-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento8,
                                                     documento='cedula_profesional.pdf', isValidado=True, notasValidado='cedP-NE', rechazoValidado='cedP-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento9,
                                                     documento='constancia_cirugia.pdf', isValidado=True, notasValidado='conC-NE', rechazoValidado='conC-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento10,
                                                     documento='carta_profesor.pdf', isValidado=True, notasValidado='carP-NE', rechazoValidado='carP-RE')
        ConvocatoriaEnroladoDocumento.objects.create(medico=medico, convocatoria=convocatoria, catTiposDocumento=catTiposDocumento12,
                                                     documento='foto.jpg', isValidado=True, notasValidado='foto-NE', rechazoValidado='foto-RE')

        ConvocatoriaEnrolado.objects.create(id=99, medico=medico, convocatoria=convocatoria, catSedes=catSedes3, catTiposExamen=catTiposExamen1)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # 10 documentos porque estudio en el extranjero envia correo de OK, se agrego la foto
        response = self.client.get('/api/convocatoria/1/medico/1/correo-documentos/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dato = ConvocatoriaEnrolado.objects.get(medico=1, convocatoria=1)
        print(f'--->>>isAceptado: {dato.isAceptado}')

        # menos de  10 documentos porque estudio en el extranjero envia correo faltantes
        ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, catTiposDocumento=9).update(isValidado=False)
        ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, catTiposDocumento=6).update(isValidado=False)
        response = self.client.get('/api/convocatoria/1/medico/1/correo-documentos/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dato = ConvocatoriaEnrolado.objects.get(medico=1, convocatoria=1)
        print(f'--->>>isAceptado: {dato.isAceptado}')

        # 9 documentos porque  es nacional envia correo de OK, se agrego la foto
        ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, catTiposDocumento=9).update(isValidado=True)
        ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, catTiposDocumento=6).update(isValidado=True)
        ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, catTiposDocumento=1).delete()
        Medico.objects.filter(id=1).update(estudioExtranjero=False)
        response = self.client.get('/api/convocatoria/1/medico/1/correo-documentos/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dato = ConvocatoriaEnrolado.objects.get(medico=1, convocatoria=1)
        print(f'--->>>isAceptado: {dato.isAceptado}')

        # menos de 9 documentos porque  es nacional envia correo faltantes
        ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, catTiposDocumento=9).update(isValidado=False)
        ConvocatoriaEnroladoDocumento.objects.filter(medico=1, convocatoria=1, catTiposDocumento=6).update(isValidado=False)
        response = self.client.get('/api/convocatoria/1/medico/1/correo-documentos/')
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dato = ConvocatoriaEnrolado.objects.get(medico=1, convocatoria=1)
        print(f'--->>>isAceptado: {dato.isAceptado}')

        # cuenta = ConvocatoriaEnroladoDocumento.objects.filter(medico=1,convocatoria=1,isValidado=True).count()
        # print(f'--->>>cuenta: {cuenta}')


class GetDescargarExcel200Test(APITestCase):
    def setUp(self):
        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion3')

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=3)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=6)
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=9)

        convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')

        ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico6, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/convocatoria/6/enrolados/bajar-excel/list/')  # regresa TODOS
        print(f'response JSON ===>>> \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutProcesaExcel200Test(APITestCase):
    def setUp(self):
        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion3')

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=3)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=6)
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=9)

        convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')

        ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico6, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3)

        archivo = open('./uploads/medicos.csv', 'rb')
        csvFile = SimpleUploadedFile(archivo.name, archivo.read(), content_type='text/csv')

        self.json = {
            "archivo": csvFile
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.put('/api/convocatoria/6/enrolados/cargar-excel/update/', data=self.json, format='multipart')  # regresa TODOS
        print(f'response JSON ===>>> \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        datos = ConvocatoriaEnrolado.objects.all()
        for dato in datos:
            print(f'--->>>id: {dato.id} - calificacion: {dato.calificacion}')


class PostSubirPago200Test(APITestCase):
    def setUp(self):
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(id=1, descripcion='tiposExameneDescripcion1', precio=111.11, precioExtrangero=222.22)
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(id=3, descripcion='tiposExameneDescripcion3', precio=333.33, precioExtrangero=444.44)

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles6')

        ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico6, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        ConvocatoriaEnrolado.objects.create(medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3, isAceptado=True)

        archivo = open('./uploads/image_4.png', 'rb')
        comprobante = SimpleUploadedFile(archivo.name, archivo.read(), content_type='image/png')

        self.json = {
            "medico": 9,
            "convocatoriaEnrolado": 3,
            "concepto": "concepto del pago",
            "comprobante": comprobante,
            "monto": 369.99,
            "nota": "nota del pago",
            # "estatus": 3
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post('/api/convocatoria/subir-pago/create/', data=self.json, format='multipart')
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cuenta = Notificacion.objects.count()
        if cuenta != 0:
            dato = Notificacion.objects.get(id=1)
            print(f'--->>>dato: titulo: {dato.titulo}, mensaje: {dato.mensaje}, destinatario: {dato.destinatario}, remitente: {dato.remitente}')


class GetPagoList200Test(APITestCase):
    def setUp(self):
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(id=1, descripcion='tiposExameneDescripcion1', precio=111.11, precioExtrangero=222.22)
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(id=3, descripcion='tiposExameneDescripcion3', precio=333.33, precioExtrangero=444.44)

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles6')

        convocatoriaEnrolado1 = ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        convocatoriaEnrolado2 = ConvocatoriaEnrolado.objects.create(medico=medico6, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        convocatoriaEnrolado3 = ConvocatoriaEnrolado.objects.create(medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3, isAceptado=True)

        Pago.objects.create(medico=medico3, convocatoriaEnrolado=convocatoriaEnrolado1, concepto='concepto', comprobante='archvivo', monto=333.33, nota='nota', estatus=3)
        Pago.objects.create(medico=medico6, convocatoriaEnrolado=convocatoriaEnrolado2, concepto='concepto', comprobante='archvivo', monto=666.66, nota='nota', estatus=2)
        Pago.objects.create(medico=medico9, convocatoriaEnrolado=convocatoriaEnrolado3, concepto='concepto', comprobante='archvivo', monto=999.99, nota='nota', estatus=1)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/convocatoria/pagos/0/list/')  # regresa TODOS
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/convocatoria/pagos/3/list/')  # regresa pendientes
        print(f'response JSON ===>>> \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutPagoAceptar200Test(APITestCase):
    def setUp(self):
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(id=1, descripcion='tiposExameneDescripcion1', precio=111.11, precioExtrangero=222.22)
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(id=3, descripcion='tiposExameneDescripcion3', precio=333.33, precioExtrangero=444.44)

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles6')

        convocatoriaEnrolado1 = ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        convocatoriaEnrolado2 = ConvocatoriaEnrolado.objects.create(medico=medico6, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        convocatoriaEnrolado3 = ConvocatoriaEnrolado.objects.create(medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3, isAceptado=True)

        Pago.objects.create(id=3, medico=medico3, convocatoriaEnrolado=convocatoriaEnrolado1, concepto='concepto', comprobante='archvivo', monto=333.33, nota='nota', estatus=3)
        Pago.objects.create(id=6, medico=medico6, convocatoriaEnrolado=convocatoriaEnrolado2, concepto='concepto', comprobante='archvivo', monto=666.66, nota='nota', estatus=3)
        Pago.objects.create(id=9, medico=medico9, convocatoriaEnrolado=convocatoriaEnrolado3, concepto='concepto', comprobante='archvivo', monto=999.99, nota='nota', estatus=3)

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated - IsAdminUser

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = Pago.objects.get(id=9)
        print(f'--->>>ANTES Pago: {dato.id} - {dato.estatus}')
        dato = ConvocatoriaEnrolado.objects.get(id=3)
        print(f'--->>>ANTES ConvocatoriaEnrolado: {dato.id} - {dato.isPagado}')

        response = self.client.put('/api/convocatoria/pago/aceptar/9/')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Pago.objects.get(id=9)
        print(f'--->>>DESPUES Pago: {dato.id} - {dato.estatus}')
        dato = ConvocatoriaEnrolado.objects.get(id=3)
        print(f'--->>>DESPUES ConvocatoriaEnrolado: {dato.id} - {dato.isPagado}')

        ConvocatoriaEnrolado.objects.filter(id=3).update(isAceptado=False)
        response = self.client.put('/api/convocatoria/pago/aceptar/9/')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        response = self.client.put('/api/convocatoria/pago/aceptar/99/')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PutPagoRechazar200Test(APITestCase):
    def setUp(self):
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(id=1, descripcion='tiposExameneDescripcion1', precio=111.11, precioExtrangero=222.22)
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(id=3, descripcion='tiposExameneDescripcion3', precio=333.33, precioExtrangero=444.44)

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', estudioExtranjero=True)

        convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona6', detalles='detalles6')

        convocatoriaEnrolado1 = ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        convocatoriaEnrolado2 = ConvocatoriaEnrolado.objects.create(medico=medico6, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1)
        convocatoriaEnrolado3 = ConvocatoriaEnrolado.objects.create(medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3, isAceptado=True)

        Pago.objects.create(id=3, medico=medico3, convocatoriaEnrolado=convocatoriaEnrolado1, concepto='concepto', comprobante='archvivo', monto=333.33, nota='nota', estatus=3)
        Pago.objects.create(id=6, medico=medico6, convocatoriaEnrolado=convocatoriaEnrolado2, concepto='concepto', comprobante='archvivo', monto=666.66, nota='nota', estatus=3)
        Pago.objects.create(id=9, medico=medico9, convocatoriaEnrolado=convocatoriaEnrolado3, concepto='concepto', comprobante='archvivo', monto=999.99, nota='nota', estatus=3)

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated - IsAdminUser

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = Pago.objects.get(id=9)
        print(f'--->>>ANTES Pago: {dato.id} - {dato.estatus}')
        dato = ConvocatoriaEnrolado.objects.get(id=3)
        print(f'--->>>ANTES ConvocatoriaEnrolado: {dato.id} - {dato.isPagado}')

        response = self.client.put('/api/convocatoria/pago/rechazar/9/')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Pago.objects.get(id=9)
        print(f'--->>>DESPUES Pago: {dato.id} - {dato.estatus}')
        dato = ConvocatoriaEnrolado.objects.get(id=3)
        print(f'--->>>DESPUES ConvocatoriaEnrolado: {dato.id} - {dato.isPagado}')

        ConvocatoriaEnrolado.objects.filter(id=3).update(isAceptado=False)
        response = self.client.put('/api/convocatoria/pago/rechazar/9/')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        response = self.client.put('/api/convocatoria/pago/rechazar/99/')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class GetPublicarCalificaciones200Test(APITestCase):
    def setUp(self):
        catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes3 = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen1 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')
        catTiposExamen3 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion3')

        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='elianid@mb.company', numRegistro=3)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='laura@mb.company', numRegistro=6)
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=9)

        convocatoria1 = Convocatoria.objects.create(id=1, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')
        convocatoria6 = Convocatoria.objects.create(id=6, fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06',
                                                    horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1')

        ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1, calificacion=10)
        ConvocatoriaEnrolado.objects.create(medico=medico6, convocatoria=convocatoria6, catSedes=catSedes1, catTiposExamen=catTiposExamen1, calificacion=5)
        ConvocatoriaEnrolado.objects.create(medico=medico9, convocatoria=convocatoria6, catSedes=catSedes3, catTiposExamen=catTiposExamen3, calificacion=69)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/convocatoria/66/enrolados/publicar/list/')  # regresa TODOS
        print(f'response JSON ===>>> \n {response.content} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



# ES DE PRUEBA NO USAR!!!
# class PostConvocatoriaSede200Test(APITestCase):
#     def setUp(self):
#         CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
#         CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
#         CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

#         CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
#         CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')

#         self.convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona1', detalles='detalles1',
#                                     )

#         self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

#         self.json = {
#             "catSedes": [1, 2]
#         }

#     def test(self):
#         self.client.force_authenticate(user=self.user)

#         response = self.client.post('/api/convocatoria/1/sede/create/', data=json.dumps(self.json), content_type="application/json")
#         # print(f'response JSON ===>>> \n {json.dumps(response.content)} \n ---')
#         # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         datos = Sede.objects.filter(convocatoria=self.convocatoria)
#         print(f'--->>>datos: {datos}')
#         for dato in datos:
#             print(dato.catSedes.descripcion)


class baseDatosTest(APITestCase):
    def setUp(self):
        CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.235698, longitud=-111.235689)
        CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.235698, longitud=-222.235689)
        catSedes = CatSedes.objects.create(descripcion='sedeDescripcion3', direccion='sedeDireccion3', latitud=33.235698, longitud=-333.235689)

        catTiposExamen = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
        CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion2')

        convocatoria = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09',
                                                   nombre='convocatoria chingona', archivo='pdfFile', banner='pngFile', detalles='detalles', )

        medico = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        ConvocatoriaEnrolado.objects.create(medico=medico, convocatoria=convocatoria, catSedes=catSedes, catTiposExamen=catTiposExamen)

    def test(self):
        # datoConvocatoria = Convocatoria.objects.get(id=1)
        # print(f'--->>>dato: {datoConvocatoria}')
        # serializer = ConvocatoriaSerializer(data=datoConvocatoria)
        # print(f'--->>>serializer: {serializer}')
        # if serializer.is_valid():
        #     # print(f'--->>>dato: {serializer.data}')
        #     print(set(serializer.data.keys()))
        # print(f'--->>>dato: {serializer.errors}')

        response = self.client.get('/api/convocatoria/ficha-registro-pdf/1/')
