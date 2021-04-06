from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json
from rest_framework import status


from preregistro.models import Medico
from recertificacion.models import *


# Create your tests here.
class GetCertificadoDatos200Test(APITestCase):
    def setUp(self):
        medico1 = Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company', numRegistro=369)

        Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=False, anioCertificacion=2000)
        Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=True, anioCertificacion=2000)
        Certificado.objects.create(medico=medico1, documento='certificado_de_chingon.PDF', descripcion='es un chingo el tipo', isVencido=True, anioCertificacion=2000)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/recertificacion/medico/1/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        Certificado.objects.filter(id=1).update(anioCertificacion=2021) # para revisar que esta vigente
        response = self.client.get('/api/recertificacion/medico/1/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        Certificado.objects.filter(id=1).update(anioCertificacion=2017) # para revisar que esta por vencer
        response = self.client.get('/api/recertificacion/medico/1/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)