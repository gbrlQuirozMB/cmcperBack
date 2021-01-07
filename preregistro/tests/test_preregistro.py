
import json
from preregistro.models import Medico
from django.http import response
from rest_framework import status
from rest_framework.test import APITestCase

nl = '\n'


class Post201Test(APITestCase):
    def setUp(self):
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

    def test(self):
        response = self.client.post('/api/preregistro/create/', data=self.json)
        print(f'response JSON ===>>> {nl} {response.data} {nl} ---')
        # print(f'response JSON ===>>> {nl} {json.loads(response.content)} {nl} ---')
        # print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medico.objects.count(), 1)
        self.assertEqual(Medico.objects.get().nombre, 'gabriel')


class Post400Test(APITestCase):
    def setUp(self):
        self.json = {
            # "nombre": "gabriel",
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

    def test(self):
        response = self.client.post('/api/preregistro/create/', data=self.json)
        print(f'response JSON ===>>> {nl} {response.data} {nl} ---')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetList200Test(APITestCase):
    def setUp(self):
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

    def test(self):
        self.client.post('/api/preregistro/create/', data=self.json)
        self.client.post('/api/preregistro/create/', data=self.json)
        self.client.post('/api/preregistro/create/', data=self.json)
        self.client.post('/api/preregistro/create/', data=self.json)
        self.client.post('/api/preregistro/create/', data=self.json)

        response = self.client.get('/api/preregistro/list/')
        print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')

        response = self.client.get(
            '/api/preregistro/list/?size=3&page=1&orderby=id&direc=asc')
        print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')

        response = self.client.get(
            '/api/preregistro/list/?size=3&page=2&orderby=id&direc=asc')
        print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetDetail200Test(APITestCase):
    def setUp(self):
        Medico.objects.create(id=1, nombre='n1', apPaterno='app1', apMaterno='apm1', rfc='rfc1', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1', deleMuni='deleMuni1',
                              colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1', cedEspecialidad='cedEspecialidad1',
                              cedCirugiaGral='cedCirugiaGral1',hospitalResi='hospitalResi1',telJefEnse='telJefEnse1',fechaInicioResi='1999-06-06',fechaFinResi='2000-07-07',telCelular='telCelular1',
                              telParticular='telParticular1',email='email1')
        Medico.objects.create(id=2, nombre='n2', apPaterno='app2', apMaterno='apm2', rfc='rfc2', curp='curp2', fechaNac='2020-09-09', pais='pais2', estado='estado2', ciudad='ciudad2', deleMuni='deleMuni2',
                              colonia='colonia', calle='calle2', cp='cp2', numExterior='numExterior2', rfcFacturacion='rfcFacturacion2', cedProfesional='cedProfesional2', cedEspecialidad='cedEspecialidad2',
                              cedCirugiaGral='cedCirugiaGral2',hospitalResi='hospitalResi2',telJefEnse='telJefEnse2',fechaInicioResi='1999-06-06',fechaFinResi='2000-07-07',telCelular='telCelular2',
                              telParticular='telParticular2',email='email2')
        Medico.objects.create(id=3, nombre='n3', apPaterno='app3', apMaterno='apm3', rfc='rfc3', curp='curp3', fechaNac='2020-09-09', pais='pais3', estado='estado3', ciudad='ciudad3', deleMuni='deleMuni3',
                              colonia='colonia', calle='calle3', cp='cp3', numExterior='numExterior3', rfcFacturacion='rfcFacturacion3', cedProfesional='cedProfesional3', cedEspecialidad='cedEspecialidad3',
                              cedCirugiaGral='cedCirugiaGral3',hospitalResi='hospitalResi3',telJefEnse='telJefEnse3',fechaInicioResi='1999-06-06',fechaFinResi='2000-07-07',telCelular='telCelular3',
                              telParticular='telParticular3',email='email3')

    def test(self):
        response = self.client.get('/api/preregistro/detail/2/')
        print(f'response JSON ===>>> {nl} {response.data} {nl} ---')
