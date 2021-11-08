from .models import *

from django.test import TestCase
from preregistro.models import Medico
from rest_framework.test import APITestCase
from datetime import date
from rest_framework import status
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
import json


# Create your tests here.

class GetCertificadosFilteredList200Test(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=333)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=666)
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999)

        Certificado.objects.create(medico=medico6, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=1)
        Certificado.objects.create(medico=medico3, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=2)
        Certificado.objects.create(medico=medico9, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=1)
        Certificado.objects.create(medico=medico3, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=2)
        Certificado.objects.create(medico=medico6, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=1)
        Certificado.objects.create(medico=medico9, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=3, documento='ya_hay_algo.pdf')

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        # response = self.client.get('/api/recertificacion/certificados/list/')
        # print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/certificados/list/?nombreNS=gabriel')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/api/certificados/list/?estatus=3')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutCertificadoCargaMasiva200Test(APITestCase):
    def setUp(self):
        medico3 = Medico.objects.create(
            id=3, nombre='elianid', apPaterno='tolentino', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=333)
        medico6 = Medico.objects.create(
            id=6, nombre='laura', apPaterno='cabrera', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=666)
        medico9 = Medico.objects.create(
            id=9, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=999)

        Certificado.objects.create(medico=medico6, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=1)
        Certificado.objects.create(medico=medico3, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=2)
        Certificado.objects.create(medico=medico9, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=1)
        Certificado.objects.create(medico=medico3, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=2)
        Certificado.objects.create(medico=medico6, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=1)
        Certificado.objects.create(medico=medico9, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=3, documento='ya_hay_algo.pdf')

        archivo = open('./uploads/testUnit.pdf', 'rb')
        certificado = SimpleUploadedFile(archivo.name, archivo.read(), content_type='application/pdf')

        self.json = {
            "documento": certificado
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = Certificado.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.medico.nombre} - {dato.documento}')

        response = self.client.put('/api/certificados/1/subir-documento/update/', data=self.json, format='multipart')
        # print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Certificado.objects.get(id=1)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.medico.nombre} - {dato.documento}')
