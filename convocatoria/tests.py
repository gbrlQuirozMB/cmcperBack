from preregistro.models import Medico
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status


# Create your tests here.
class PutEsExtranjero200Test(APITestCase):
    def setUp(self):
        Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

        self.json = {
            "isExtranjero": True,
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