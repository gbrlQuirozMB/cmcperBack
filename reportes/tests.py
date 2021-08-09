from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import json
from rest_framework import status

from preregistro.models import *
from catalogos.models import *
from convocatoria.models import *


def configDB():
    Medico.objects.create(
        nombre='elianid', apPaterno='tolentino', apMaterno='tolentino', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', email='elianid@mb.company', numRegistro=111, aceptado=True, telConsultorio='telConsultorio1', sexo='F', isCertificado=True)
    Medico.objects.create(
        nombre='laura grissel', apPaterno='cabrera', apMaterno='bejarano', rfc='quog??0406', curp='curp2', fechaNac='2020-09-09', pais='pais2', estado='estado2', ciudad='ciudad2',
        deleMuni='deleMuni2', colonia='colonia', calle='calle2', cp='cp2', numExterior='numExterior2', rfcFacturacion='rfcFacturacion2', cedProfesional='cedProfesional2',
        cedEspecialidad='cedEspecialidad2', cedCirugiaGral='cedCirugiaGral2', hospitalResi='hospitalResi2', telJefEnse='telJefEnse2', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular2', telParticular='telParticular2', email='laura@mb.company', numRegistro=222, aceptado=False, telConsultorio='telConsultorio2', sexo='F', isCertificado=True)
    medico3 = Medico.objects.create(
        nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp3', fechaNac='2020-09-09', pais='pais3', estado='estado3', ciudad='ciudad3',
        deleMuni='deleMuni3', colonia='colonia', calle='calle3', cp='cp3', numExterior='numExterior3', rfcFacturacion='rfcFacturacion3', cedProfesional='cedProfesional3',
        cedEspecialidad='cedEspecialidad3', cedCirugiaGral='cedCirugiaGral3', hospitalResi='hospitalResi3', telJefEnse='telJefEnse3', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular3', telParticular='telParticular3', email='gabriel@mb.company', numRegistro=333, aceptado=True, telConsultorio='telConsultorio3', sexo='M', isCertificado=False)
    medico4 = Medico.objects.create(
        nombre='gisela', apPaterno='paredes', apMaterno='cruz', rfc='quog??0406', curp='curp4', fechaNac='2020-09-09', pais='pais4', estado='estado4', ciudad='ciudad4',
        deleMuni='deleMuni4', colonia='colonia', calle='calle4', cp='cp4', numExterior='numExterior4', rfcFacturacion='rfcFacturacion4', cedProfesional='cedProfesional4',
        cedEspecialidad='cedEspecialidad4', cedCirugiaGral='cedCirugiaGral4', hospitalResi='hospitalResi4', telJefEnse='telJefEnse4', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular4', telParticular='telParticular4', email='gisela@mb.company', numRegistro=444, aceptado=True, telConsultorio='telConsultorio4', sexo='F', isCertificado=True)
    Medico.objects.create(
        nombre='miguel', apPaterno='vargas', apMaterno='aranda', rfc='quog??0506', curp='curp5', fechaNac='2020-09-09', pais='pais5', estado='estado5', ciudad='ciudad5',
        deleMuni='deleMuni5', colonia='colonia', calle='calle5', cp='cp5', numExterior='numExterior5', rfcFacturacion='rfcFacturacion5', cedProfesional='cedProfesional5',
        cedEspecialidad='cedEspecialidad5', cedCirugiaGral='cedCirugiaGral5', hospitalResi='hospitalResi5', telJefEnse='telJefEnse5', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular5', telParticular='telParticular5', email='gabriel@mb.company', numRegistro=555, aceptado=True, telConsultorio='telConsultorio5', sexo='M', isCertificado=True)
    Medico.objects.create(
        nombre='pedro', apPaterno='gallegos', apMaterno='rodriguez', rfc='quog??0606', curp='curp6', fechaNac='2020-09-09', pais='pais6', estado='estado6', ciudad='ciudad6',
        deleMuni='deleMuni6', colonia='colonia', calle='calle6', cp='cp6', numExterior='numExterior6', rfcFacturacion='rfcFacturacion6', cedProfesional='cedProfesional6',
        cedEspecialidad='cedEspecialidad6', cedCirugiaGral='cedCirugiaGral6', hospitalResi='hospitalResi6', telJefEnse='telJefEnse6', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular6', telParticular='telParticular6', email='gabriel@mb.company', numRegistro=666, aceptado=True, telConsultorio='telConsultorio6', sexo='M', isCertificado=False)

    catSedes1 = CatSedes.objects.create(descripcion='sedeDescripcion1', direccion='sedeDireccion1', latitud=11.111111, longitud=-111.111111)
    catSedes2 = CatSedes.objects.create(descripcion='sedeDescripcion2', direccion='sedeDireccion2', latitud=22.222222, longitud=-222.222222)

    catTiposExamen1 = CatTiposExamen.objects.create(descripcion='Normal', precio=11.11, precioExtrangero=111.11)
    catTiposExamen2 = CatTiposExamen.objects.create(descripcion='Especial', precio=22.22, precioExtrangero=222.22)

    # catTiposExamen1 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion1')
    # catTiposExamen2 = CatTiposExamen.objects.create(descripcion='tiposExameneDescripcion3')

    convocatoria1 = Convocatoria.objects.create(fechaInicio='2020-06-04', fechaTermino='2021-02-11', fechaExamen='2021-04-06', horaExamen='09:09', nombre='convocatoria chingona1',
                                                detalles='detalles1')

    ConvocatoriaEnrolado.objects.create(medico=medico3, convocatoria=convocatoria1, catSedes=catSedes2, catTiposExamen=catTiposExamen2, calificacion=9, isAprobado=True, isPublicado=False)
    ConvocatoriaEnrolado.objects.create(medico=medico4, convocatoria=convocatoria1, catSedes=catSedes1, catTiposExamen=catTiposExamen1, calificacion=5, isAprobado=True, isPublicado=False)


class GetMedResidenteFilteredListTest(APITestCase):
    def setUp(self):
        configDB()
        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/reportes/med-residentes/list/')
        print(f'response JSON ===>>> obtiene solo lo residentes (isCertificado=False) \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ponemos todos lo registros como residentes
        Medico.objects.all().update(isCertificado=False)

        response = self.client.get('/api/reportes/med-residentes/list/?telConsultorioNS=rio1')
        print(f'response JSON ===>>> telConsutorioNS=rio1 \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/reportes/med-residentes/list/?sexo=F')
        print(f'response JSON ===>>> sexo=F \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # # buscar en un solo campo de entrada separados por comas
        # response = self.client.get('/api/reportes/med-residentes/list/?nombreCompletoNS=laura grissel,cabrera,bejarano')
        # print(f'response JSON ===>>> nombreCompletoNS=laura grissel,cabrera,bejarano \n {json.dumps(response.json())} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        # buscar en cada uno de los campos nombre, apPaterno y apMaterno
        response = self.client.get('/api/reportes/med-residentes/list/?nombre=laura grissel&apPaterno=cabrera&apMaterno=bejarano')
        print(f'response JSON ===>>> nombre=laura grissel&apPaterno=cabrera&apMaterno=bejarano \n {json.dumps(response.json())} \n ---')
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
