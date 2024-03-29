# from dateutil import relativedelta
from dateutil.relativedelta import relativedelta

from .models import *

from django.test import TestCase
from preregistro.models import Medico
from certificados.models import Certificado
from rest_framework.test import APITestCase
from datetime import date
from rest_framework import status
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import json


def configDB():
    medico3 = Medico.objects.create(
        id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=333, diplomaConacem='Pone Dora')
    medico6 = Medico.objects.create(
        id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=666, diplomaConacem='GlandM Enormes')
    medico9 = Medico.objects.create(
        id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999, diplomaConacem='Yo mero')
    medico5 = Medico.objects.create(
        id=5, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
        deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
        cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
        telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999, diplomaConacem='XXX')

    Certificado.objects.create(medico=medico3, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                               fechaCaducidad=date.today()+relativedelta(years=5), estatus=1)
    Certificado.objects.create(medico=medico3, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                               fechaCaducidad=date.today()+relativedelta(years=5), estatus=2, isConacem=True)
    Certificado.objects.create(medico=medico9, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                               fechaCaducidad=date.today()+relativedelta(years=5), estatus=1)
    Certificado.objects.create(medico=medico3, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                               fechaCaducidad=date.today()+relativedelta(years=5), estatus=2, isConacem=True)
    Certificado.objects.create(medico=medico6, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                               fechaCaducidad=date.today()+relativedelta(years=5), estatus=1)
    Certificado.objects.create(medico=medico5, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                               fechaCaducidad=date.today()+relativedelta(years=5), estatus=3, documento='ya_hay_algo.pdf', isConacem=False)


class GetConacemListTest(APITestCase):
    def setUp(self):
        configDB()
        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/conacem/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostConacemTest(APITestCase):
    def setUp(self):
        configDB()

        self.json = {
            "fechaEnvio": "2021-04-06",
            "tituloPresidente": "dactar",
            "nombrePresidente": "gabriel quiroz",
            "tituloResponsable": "enferm",
            "nombreResponsable": "elianid tolentino",
            "fechaEmision": "2021-04-06",
            "costo": 369.33,
            "fechaValidezDel": "2021-04-06",
            "fechaValidezAl": "2021-04-06",
            "iniciaLibro": 3,
            "hoja": 3,
            "lugar": 6,
            "cupo": 9,
            "medicos": [
                {"medico": 3},
                {"medico": 6},
                {"medico": 9}
            ]
            # "medicos":[]
        }

        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):

        self.client.force_authenticate(user=self.user)

        # para revisar como esta el estatus 'isConacem' de los certificados antes
        for datoCertificado in Certificado.objects.filter().order_by('id'):
            print(f'--->>>datoCertificado.id: {datoCertificado.id} -- datoCertificado.medico.id: {datoCertificado.medico.id} -- datoCertificado.isConacem: {datoCertificado.isConacem}')

        response = self.client.post('/api/conacem/create/', data=json.dumps(self.json), content_type="application/json")
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # del self.json['nombreInstitucion']
        # response = self.client.post('/api/conacem/create/', data=json.dumps(self.json), content_type="application/json")
        # print(f'response JSON ===>>> ok \n {json.dumps(response.data)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # para revisar que este bien el libro y foja en detalles
        datosDetalle = DetalleConcacem.objects.filter()
        if datosDetalle.count() > 0:
            for dato in datosDetalle:
                print(f'--->>>detalle.medico.id: {dato.medico.id} --- libro: {dato.libro} --- foja: {dato.foja} --- detalle.nombre: {dato.medico.nombre} --- detalle.conacem.id: {dato.conacem.id}')

        # para revisar como esta el estatus 'isConacem' de los certificados antes
        print(f'\n')
        for datoCertificado in Certificado.objects.filter().order_by('id'):
            print(f'--->>>datoCertificado.id: {datoCertificado.id} -- datoCertificado.medico.id: {datoCertificado.medico.id} -- datoCertificado.isConacem: {datoCertificado.isConacem}')


class PruebaTest(APITestCase):
    def setUp(self):
        pass

    def test(self):
        hoja = 6
        lugar = 9
        cupo = 12
        tam = 29

        quedan = (cupo-lugar)
        bandera = True
        for reg in range(tam):
            print(f'--->>>reg: {reg} -- hoja: {hoja} --- lugar: {lugar}')
            lugar = lugar + 1

            if lugar > cupo:
                # print(f'--->>>BANDERA-2: {bandera} -- hoja: {hoja} --- lugar: {lugar}')
                lugar = 1
                hoja = hoja + 1
