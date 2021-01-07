
import json
from preregistro.models import Medico
from django.http import response
from rest_framework import status
from rest_framework.test import APITestCase

nl = '\n'


class Post200Test(APITestCase):
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
        
        
        response = self.client.get('/api/preregistro/list/?size=3&page=1&orderby=id&direc=asc')
        print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')
        
        
        response = self.client.get('/api/preregistro/list/?size=3&page=2&orderby=id&direc=asc')
        print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)