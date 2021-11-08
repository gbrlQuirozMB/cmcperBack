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


class GetConacemListTest(APITestCase):
    def setUp(self):
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
        Certificado.objects.create(medico=medico9, descripcion='generado automaticamente', isVencido=False, fechaCertificacion=date.today(),
                                   fechaCaducidad=date.today()+relativedelta(years=5), estatus=3, documento='ya_hay_algo.pdf', isConacem=True)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/conacem/list/')
        print(f'response JSON ===>>> ok \n {json.dumps(response.json(), ensure_ascii=False)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
