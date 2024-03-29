from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import json
from rest_framework import status

from preregistro.models import *
from catalogos.models import *
from convocatoria.models import *
from certificados.models import Certificado


from django.db.models import Q, Value
from django.db.models.functions import Concat

import datetime


def configDB():
    Medico.objects.create(
        nombre='elianid', apPaterno='tolentino', apMaterno='tolentino', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', email='elianid@mb.company', numRegistro=111, aceptado=True, telConsultorio='telConsultorio1', sexo='F',
        anioCertificacion=2022, isConsejero=True, isProfesor=False, isCertificado=True)
    Medico.objects.create(
        nombre='laura grissel', apPaterno='cabrera', apMaterno='bejarano', rfc='quog??0406', curp='curp2', fechaNac='2020-09-09', pais='pais2', estado='estado2', ciudad='ciudad2',
        deleMuni='deleMuni2', colonia='colonia', calle='calle2', cp='cp2', numExterior='numExterior2', rfcFacturacion='rfcFacturacion2', cedProfesional='cedProfesional2',
        cedEspecialidad='cedEspecialidad2', cedCirugiaGral='cedCirugiaGral2', hospitalResi='hospitalResi2', telJefEnse='telJefEnse2', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular2', telParticular='telParticular2', email='laura@mb.company', numRegistro=222, aceptado=False, telConsultorio='telConsultorio2', sexo='F',
        anioCertificacion=2000, isConsejero=False, isProfesor=True, isCertificado=True)
    medico3 = Medico.objects.create(
        nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp3', fechaNac='2020-09-09', pais='pais3', estado='estado3', ciudad='ciudad3',
        deleMuni='deleMuni3', colonia='colonia', calle='calle3', cp='cp3', numExterior='numExterior3', rfcFacturacion='rfcFacturacion3', cedProfesional='cedProfesional3',
        cedEspecialidad='cedEspecialidad3', cedCirugiaGral='cedCirugiaGral3', hospitalResi='hospitalResi3', telJefEnse='telJefEnse3', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular3', telParticular='telParticular3', email='gabriel@mb.company', numRegistro=333, aceptado=True, telConsultorio='telConsultorio3', sexo='M',
        anioCertificacion=2022, isConsejero=True, isProfesor=False, isCertificado=False)
    medico4 = Medico.objects.create(
        nombre='gisela', apPaterno='paredes', apMaterno='cruz', rfc='quog??0406', curp='curp4', fechaNac='2020-09-09', pais='pais4', estado='estado4', ciudad='ciudad4',
        deleMuni='deleMuni4', colonia='colonia', calle='calle4', cp='cp4', numExterior='numExterior4', rfcFacturacion='rfcFacturacion4', cedProfesional='cedProfesional4',
        cedEspecialidad='cedEspecialidad4', cedCirugiaGral='cedCirugiaGral4', hospitalResi='hospitalResi4', telJefEnse='telJefEnse4', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular4', telParticular='telParticular4', email='gisela@mb.company', numRegistro=444, aceptado=True, telConsultorio='telConsultorio4', sexo='F',
        anioCertificacion=2000, isConsejero=False, isProfesor=True, isCertificado=True)
    Medico.objects.create(
        nombre='miguel', apPaterno='vargas', apMaterno='aranda', rfc='quog??0506', curp='curp5', fechaNac='2020-09-09', pais='pais5', estado='estado5', ciudad='ciudad5',
        deleMuni='deleMuni5', colonia='colonia', calle='calle5', cp='cp5', numExterior='numExterior5', rfcFacturacion='rfcFacturacion5', cedProfesional='cedProfesional5',
        cedEspecialidad='cedEspecialidad5', cedCirugiaGral='cedCirugiaGral5', hospitalResi='hospitalResi5', telJefEnse='telJefEnse5', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular5', telParticular='telParticular5', email='gabriel@mb.company', numRegistro=555, aceptado=True, telConsultorio='telConsultorio5', sexo='M',
        anioCertificacion=2000, isConsejero=False, isProfesor=True, isCertificado=True)
    medico6 = Medico.objects.create(
        nombre='pedro', apPaterno='gallegos', apMaterno='rodriguez', rfc='quog??0606', curp='curp6', fechaNac='2020-09-09', pais='pais6', estado='estado6', ciudad='ciudad6',
        deleMuni='deleMuni6', colonia='colonia', calle='calle6', cp='cp6', numExterior='numExterior6', rfcFacturacion='rfcFacturacion6', cedProfesional='cedProfesional6',
        cedEspecialidad='cedEspecialidad6', cedCirugiaGral='cedCirugiaGral6', hospitalResi='hospitalResi6', telJefEnse='telJefEnse6', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular6', telParticular='telParticular6', email='gabriel@mb.company', numRegistro=666, aceptado=True, telConsultorio='telConsultorio6', sexo='M',
        anioCertificacion=2000, isConsejero=False, isProfesor=True, isCertificado=False)

    catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.111111, longitud=-111.111111)
    catSedes2 = CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.222222, longitud=-222.222222)

    catTiposExamen1 = CatTiposExamen.objects.create(descripcion='Normal', precio=11.11, precioExtrangero=111.11)
    catTiposExamen2 = CatTiposExamen.objects.create(descripcion='Especial', precio=22.22, precioExtrangero=222.22)

    # catTiposExamen1 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
    # catTiposExamen2 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion3')

    convocatoria1 = Convocatoria.objects.create(fechaInicio='2020-04-04', fechaTermino='2021-11-11', fechaExamen='2021-04-04', horaExamen='09:09', nombre='convocatoria chingona1',
                                                detalles='detalles1')
    convocatoria2 = Convocatoria.objects.create(fechaInicio='2020-06-06', fechaTermino='2021-12-12', fechaExamen='2021-06-06', horaExamen='06:06', nombre='convocatoria chingona2',
                                                detalles='detalles2')

    ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria2, catSedes=catSedes2, catTiposExamen=catTiposExamen2, calificacion=9, isAprobado=True, isPublicado=False)
    ConvocatoriaEnrolado.objects.create(medico=medico4, convocatoria=convocatoria1, catSedes=catSedes1, catTiposExamen=catTiposExamen1, calificacion=5, isAprobado=True, isPublicado=False)

    Certificado.objects.create(medico=medico3, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=False, fechaCertificacion='2021-04-06',
                               fechaCaducidad='2026-04-06', estatus=1)
    Certificado.objects.create(medico=medico4, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=True, fechaCertificacion='2000-04-06',
                               fechaCaducidad='2005-04-06', estatus=2)
    Certificado.objects.create(medico=medico3, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=True, fechaCertificacion='2016-05-06',
                               fechaCaducidad='2021-05-06', estatus=2)


class GetMedResidenteFilteredListTest(APITestCase):
    def setUp(self):
        configDB()
        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # # Medico.objects.filter(id=3).update(isCertificado=True)
        # response = self.client.get('/api/reportes/med-residentes/list/')
        # print(f'response JSON ===>>> obtiene solo lo residentes (isCertificado=False) \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # # Medico.objects.filter(id=3).update(isCertificado=True)
        # Medico.objects.all().update(isCertificado=True)
        # response = self.client.get('/api/reportes/med-residentes/list/?isCertificado=False&nombreCompletoNS=Quiroz Olvera')
        # print(f'response JSON ===>>> obtiene solo lo residentes (isCertificado=False) \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ponemos todos lo registros como residentes
        Medico.objects.all().update(isCertificado=False)

        # response = self.client.get('/api/reportes/med-residentes/list/?isCertificado=False&sexo=F')
        # print(f'response JSON ===>>> sexo=F \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/reportes/med-residentes/list/?isCertificado=False&nombreCompletoNS=Quiroz Olvera')
        # print(f'response JSON ===>>> nombreCompletoNS=Quiroz Olvera \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Medico.objects.filter(id=3).update(creado_en='2022-08-11T14:10:40.875138-05:00')
        # response = self.client.get('/api/reportes/med-residentes/list/?isCertificado=False&anioInscr=2022')
        # print(f'response JSON ===>>> anioInscr=2022 \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get('/api/reportes/med-residentes/list/?isCertificado=False&sede=1')
        print(f'response JSON ===>>> sede=1 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get('/api/reportes/med-residentes/list/?isCertificado=False&convocatoria=1')
        print(f'response JSON ===>>> convocatoria=1 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response = self.client.get('/api/reportes/med-residentes/list/?isCertificado=False&convocatoria=2')
        print(f'response JSON ===>>> convocatoria=2 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetMedResidenteDetailTest(APITestCase):
    def setUp(self):
        configDB()
        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/reportes/med-residentes/3/detail/')
        print(f'response JSON ===>>> obtiene solo lo residentes (isCertificado=False) \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/reportes/med-residentes/1/detail/')
        print(f'response JSON ===>>> 404 (isCertificado=True) \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetMedResidenteExtraDetailTest(APITestCase):
    def setUp(self):
        configDB()
        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/reportes/med-residentes/3/extras/')
        print(f'response JSON ===>>> obtiene solo lo residentes (isCertificado=False) \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/reportes/med-residentes/1/extras/')
        print(f'response JSON ===>>> 404 (isCertificado=True) \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PutMedResidenteTest(APITestCase):
    def setUp(self):
        configDB()

        self.json = {
            "nombre": "gabriel",
            "apPaterno": "quiroz",
            "apMaterno": "olvera",
            "rfc": "quog000406",
            "curp": "quog000406CURP",
            "fechaNac": "2020-12-09",
            "pais": "mexico",
            "estado": "hidalgo",
            "ciudad": "pachuca",
            "deleMuni": "pachuca de soto",
            "colonia": "issste",
            "calle": "rio moctezuma",
            "cp": "42083",
            "numExterior": "111",
            "rfcFacturacion": "111",
            "cedProfesional": "333333",
            "cedEspecialidad": "666666",
            "cedCirugiaGral": "999999",
            "hospitalResi": "hospital del issste",
            "telJefEnse": "7719876543",
            "fechaInicioResi": "1999-06-09",
            "fechaFinResi": "2000-07-10",
            "telCelular": "7711896189",
            "telParticular": "7711234567",
            "email": "doctor@medico.com"
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # response = self.client.put('/api/reportes/med-residentes/3/update/', data=json.dumps(self.json), content_type="application/json")
        # print(f'response JSON ===>>> obtiene solo lo residentes (isCertificado=False) \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.put('/api/reportes/med-residentes/1/update/', data=json.dumps(self.json), content_type="application/json")
        # print(f'response JSON ===>>> 404 (isCertificado=True) \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # se reutiliza en endpoint ya existente
        response = self.client.put('/api/preregistro/update/3/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetMedCertificadoFilteredListTest(APITestCase):
    def setUp(self):
        configDB()
        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/reportes/med-certificados/list/')
        print(f'response JSON ===>>> obtiene solo lo certificados (isCertificado=True) \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ponemos todos lo registros como certificados
        Medico.objects.all().update(isCertificado=True)

        response = self.client.get('/api/reportes/med-certificados/list/?isCertificado=True&numRegistro=333')
        print(f'response JSON ===>>> numRegistro=333 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/reportes/med-certificados/list/?isCertificado=True&nombreCompletoNS=Quiroz Olvera')
        print(f'response JSON ===>>> nombreCompletoNS=Quiroz Olvera \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/reportes/med-certificados/list/?isCertificado=True&estatus=1')
        print(f'response JSON ===>>> estatus=1 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/reportes/med-certificados/list/?isCertificado=True&estatus=1&numRegistro=333')
        print(f'response JSON ===>>> estatus=1&numRegistro=333 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/reportes/med-certificados/list/?isCertificado=True&anioCertificacion=2022')
        print(f'response JSON ===>>> anioCertificacion=2022 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/reportes/med-certificados/list/?isCertificado=True&isCertificado=True&isConsejero=True')
        print(f'response JSON ===>>> isConsejero=True \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/reportes/med-certificados/list/?isCertificado=True&isProfesor=True')
        print(f'response JSON ===>>> isProfesor=True7 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # queryset = Medico.objects.annotate(completo=Concat('nombre', Value(' '), 'apPaterno', Value(' '), 'apMaterno')).filter(completo__icontains='gabriel quiroz').values('nombre')
        # print(f'--->>>SQL: {queryset.query}')

        # dato = Certificado.objects.filter(medico=3)[0]
        # print(f'--->>>dato: {dato}')
        # print(f'--->>>dato: {dato.get_estatus_display()}')

        # for dato in Certificado.objects.filter(medico=3):
        #     print(f'--->>>datos.medico.nombre: {dato.medico.nombre}')

        # anio = datetime.date.today().year
        # print(f'--->>>anio: {anio} - type: {type(anio)}')


class GetMedCertificadoFechasTest(APITestCase):
    def setUp(self):
        configDB()
        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/reportes/med-certificados/3/fecha-ultima-certificacion/')
        print(f'response JSON ===>>> obtiene solo lo certificados (isCertificado=True) \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/reportes/med-certificados/1/fecha-ultima-certificacion/')
        print(f'response JSON ===>>> 404 (isCertificado=True) \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# class GetPruebaPdf(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated
        
#     def test(self):
#         self.client.force_authenticate(user=self.user)
        
#         response = self.client.get('/api/reportes/pruebas/36/pdf/')
#         print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)