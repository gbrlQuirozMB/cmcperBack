
import json
from notificaciones.models import Notificacion

from django.contrib.auth.models import User
from preregistro.models import Medico
from django.http import response
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile


nl = '\n'


class Post201Test(APITestCase):
    def setUp(self):
        User.objects.create_user(username='limitado', email='limitado@cmcper.com', password='password', first_name='Juanito', last_name='Perez')
        User.objects.create_user(username='normal', email='normal@cmcper.com', password='password', first_name='Panchito', last_name='Sanchez')
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

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
        print(f'response JSON ===>>> {nl} {response.content} {nl} ---')
        # print(f'response JSON ===>>> {nl} {json.loads(response.content)} {nl} ---')
        # print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medico.objects.count(), 1)
        self.assertEqual(Medico.objects.get().nombre, 'gabriel')

        queryset = Notificacion.objects.all()
        print(f'queryset: {queryset}')
        for dato in queryset:
            print(f'--->>>dato: titulo: {dato.titulo}, mensaje: {dato.mensaje}, destinatario: {dato.destinatario}, remitente: {dato.remitente}')


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
        User.objects.create_user(username='limitado', email='limitado@cmcper.com', password='password', first_name='Juanito', last_name='Perez')
        User.objects.create_user(username='normal', email='normal@cmcper.com', password='password', first_name='Panchito', last_name='Sanchez')
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

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

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

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
        Medico.objects.create(id=1, nombre='n1', apPaterno='app1', apMaterno='apm1', rfc='rfc1', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
                              deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
                              cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06',
                              fechaFinResi='2000-07-07', telCelular='telCelular1', telParticular='telParticular1', email='email1')
        Medico.objects.create(id=2, nombre='n2', apPaterno='app2', apMaterno='apm2', rfc='rfc2', curp='curp2', fechaNac='2020-09-09', pais='pais2', estado='estado2', ciudad='ciudad2',
                              deleMuni='deleMuni2', colonia='colonia', calle='calle2', cp='cp2', numExterior='numExterior2', rfcFacturacion='rfcFacturacion2', cedProfesional='cedProfesional2',
                              cedEspecialidad='cedEspecialidad2', cedCirugiaGral='cedCirugiaGral2', hospitalResi='hospitalResi2', telJefEnse='telJefEnse2', fechaInicioResi='1999-06-06',
                              fechaFinResi='2000-07-07', telCelular='telCelular2', telParticular='telParticular2', email='email2')
        Medico.objects.create(id=3, nombre='n3', apPaterno='app3', apMaterno='apm3', rfc='rfc3', curp='curp3', fechaNac='2020-09-09', pais='pais3', estado='estado3', ciudad='ciudad3',
                              deleMuni='deleMuni3', colonia='colonia', calle='calle3', cp='cp3', numExterior='numExterior3', rfcFacturacion='rfcFacturacion3', cedProfesional='cedProfesional3',
                              cedEspecialidad='cedEspecialidad3', cedCirugiaGral='cedCirugiaGral3', hospitalResi='hospitalResi3', telJefEnse='telJefEnse3', fechaInicioResi='1999-06-06',
                              fechaFinResi='2000-07-07', telCelular='telCelular3', telParticular='telParticular3', email='email3', fotoPerfil='mi_foto_999.png')
        
        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated
        

    def test(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.get('/api/preregistro/detail/3/')
        print(f'response JSON ===>>> {nl} {response.data} {nl} ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PutAceptar200Test(APITestCase):
    def setUp(self):
        User.objects.create_user(username='limitado', email='limitado@cmcper.com', password='password', first_name='Juanito', last_name='Perez')
        User.objects.create_user(username='normal', email='normal@cmcper.com', password='password', first_name='Panchito', last_name='Sanchez')
        User.objects.create_user(username='admin', email='admin@cmcper.com', password='password', first_name='Enrique', last_name='Lucero', is_superuser=True, is_staff=True)

        Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog??0406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')
        self.json = {
            "motivo": "este es el motivo de aceptacion"
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)
        # como esta originalmente
        # response = self.client.get('/api/preregistro/detail/1/')
        # print(f'response JSON ===>>> {nl} {response.data} {nl} ---')
        # se hace la aprobacion
        response = self.client.put('/api/preregistro/aceptar/1/', self.json)
        print(f'response JSON ===>>> {nl} {response.data} {nl} ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # como queda despues
        # response = self.client.get('/api/preregistro/detail/1/')
        # print(f'response JSON ===>>> {nl} {response.data} {nl} ---')

        dato = Medico.objects.get(id=1)
        print(f'--->>>dato: {dato.id} - {dato.motivo} - {dato.aceptado} - {dato.numRegistro}')

        # que el usuario se haya creado correctamente
        self.assertEqual(User.objects.count(), 5)
        self.assertEqual(User.objects.get(id=5).email, 'gabriel@mb.company')
        queryset = User.objects.filter(id=5)
        for dato in queryset:
            print(f'username: {dato.username}')
            print(f'email: {dato.email}')
            print(f'password: {dato.password}')
            print(f'first_name: {dato.first_name}')
            print(f'last_name: {dato.last_name}')
            print(f'user_permissions: {dato.get_user_permissions()}')

        # que la notificaion este correcta
        queryset = Notificacion.objects.all()
        for dato in queryset:
            print(f'--->>>dato: titulo: {dato.titulo}, mensaje: {dato.mensaje}, destinatario: {dato.destinatario}, remitente: {dato.remitente}')


class PutRechazar200Test(APITestCase):
    def setUp(self):
        Medico.objects.create(id=1, nombre='n1', apPaterno='app1', apMaterno='apm1', rfc='rfc1', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
                              deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
                              cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06',
                              fechaFinResi='2000-07-07', telCelular='telCelular1', telParticular='telParticular1', email='email1')
        self.json = {
            "motivo": "este es el motivo de rechazo"
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)
        # response = self.client.get('/api/preregistro/detail/1/')
        # print(f'response JSON ===>>> {nl} {response.data} {nl} ---')

        response = self.client.put('/api/preregistro/rechazar/1/', self.json)
        print(f'response JSON ===>>> {nl} {response.data} {nl} ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # response = self.client.get('/api/preregistro/detail/1/')
        # print(f'response JSON ===>>> {nl} {response.data} {nl} ---')

        # no hay notificacion porque estas son dentro del sistema
        dato = Medico.objects.get(id=1)
        print(f'--->>>dato: {dato.id} - {dato.motivo} - {dato.aceptado} - {dato.numRegistro}')


class PutFotoPerfil200Test(APITestCase):
    def setUp(self):
        Medico.objects.create(id=1, nombre='n1', apPaterno='app1', apMaterno='apm1', rfc='rfc1', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
                              deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
                              cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06',
                              fechaFinResi='2000-07-07', telCelular='telCelular1', telParticular='telParticular1', email='email1')

        archivo = open('./uploads/banner.png', 'rb')
        imgFile = SimpleUploadedFile(archivo.name, archivo.read(), content_type='image/png')

        self.json = {
            "fotoPerfil": imgFile
        }

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        dato = Medico.objects.get(id=1)
        print(f'--->>>ANTES dato: {dato.id} - {dato.nombre} - {dato.fotoPerfil}')

        response = self.client.put('/api/preregistro/medico/1/foto-perfil/', data=self.json, format='multipart')
        print(f'response JSON ===>>> \n {response.data} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        dato = Medico.objects.get(id=1)
        print(f'--->>>DESPUES dato: {dato.id} - {dato.nombre} - {dato.fotoPerfil}')


class baseDatosTest(APITestCase):
    def setUp(self):
        Medico.objects.create(
            id=1, nombre='gabriel', apPaterno='quiroz', apMaterno='olvera', rfc='quog760406', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1',
            deleMuni='deleMuni1', colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1',
            cedEspecialidad='cedEspecialidad1', cedCirugiaGral='cedCirugiaGral1', hospitalResi='hospitalResi1', telJefEnse='telJefEnse1', fechaInicioResi='1999-06-06', fechaFinResi='2000-07-07',
            telCelular='telCelular1', telParticular='telParticular1', email='gabriel@mb.company')

    def test(self):
        # creando valores para crear usuarios
        # user = User.objects.create_user(username=username,email=datosMedico[0][3],password=password,first_name=datosMedico[0][0],last_name=datosMedico[0][1])

        datosMedico = Medico.objects.filter(id=1).values_list('nombre', 'apPaterno', 'apMaterno', 'email', 'rfc')
        nombre = str(datosMedico[0][0] + ' ' + datosMedico[0][1] + ' ' + datosMedico[0][2])
        username = datosMedico[0][0][0:3] + datosMedico[0][1][0:3] + datosMedico[0][4][4:6]

        print(username)
