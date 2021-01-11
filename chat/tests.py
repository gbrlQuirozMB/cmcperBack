from rest_framework.test import APITestCase
from .models import *
from preregistro.models import *
from rest_framework import status

nl = '\n'


# Create your tests here.
class baseDatosTest(APITestCase):
    def setUp(self):
        Mensaje.objects.create(mensaje='mensaje1',destinatario=111,remitente=369)
        Mensaje.objects.create(mensaje='mensaje2',destinatario=222,remitente=369)
        Mensaje.objects.create(mensaje='mensaje3',destinatario=333,remitente=369)
        Conversacion.objects.create(nombre='nombre1',destinatario=111)
        Conversacion.objects.create(nombre='nombre2',destinatario=222)
        Conversacion.objects.create(nombre='nombre3',destinatario=333)
    
    def test(self):
        # crear mensaje nuevo
        Mensaje.objects.create(mensaje='mensajeX',destinatario=222,remitente=369)
        Conversacion.objects.filter(destinatario=222).delete()
        Conversacion.objects.create(nombre='nombreX',destinatario=222)
        
        queryset = Mensaje.objects.filter(remitente=369)
        print(queryset)
        # print(f'{queryset.query} {nl} --- {nl}')
        for dato in queryset:
            print(f'mensaje: {dato.mensaje}')
        
        queryset2 = Conversacion.objects.all()    
        print(queryset2)
        for dato in queryset2:
            print(f'conversacion: {dato.nombre}')
            
            
class Post201Test(APITestCase):
    def setUp(self):
        Mensaje.objects.create(mensaje='mensaje1',destinatario=111,remitente=369)
        Mensaje.objects.create(mensaje='mensaje2',destinatario=222,remitente=369)
        Mensaje.objects.create(mensaje='mensaje3',destinatario=333,remitente=369)
        Conversacion.objects.create(nombre='nombre1',destinatario=111)
        Conversacion.objects.create(nombre='nombre2',destinatario=222)
        Conversacion.objects.create(nombre='nombre3',destinatario=333)
        Medico.objects.create(nombre='n1', apPaterno='app1', apMaterno='apm1', rfc='rfc1', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1', deleMuni='deleMuni1',
                        colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1', cedEspecialidad='cedEspecialidad1',
                        cedCirugiaGral='cedCirugiaGral1',hospitalResi='hospitalResi1',telJefEnse='telJefEnse1',fechaInicioResi='1999-06-06',fechaFinResi='2000-07-07',telCelular='telCelular1',
                        telParticular='telParticular1',email='email1', numRegistro=222)
        self.json = {
            "mensaje": "mesaje del json",
            "destinatario": 222,
            "remitente": 369
        }
        
    def test(self):
        
        conSesion = False #True-> mandamos variable de sesion para poner en la DB, False-> como no existe la sesion se obtiene de la DB y se pone en sesion
        
        if conSesion:
            sesion = self.client.session
            sesion["nombre"] = 'gabriel quiroz'
            sesion.save()
        
        response = self.client.post('/api/chat/create/', data=self.json)
        print(f'response JSON ===>>> {nl} {response.data} {nl} ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conversacion.objects.count(), 3) # debe ser 3 porque se borra el que existe
        
        if conSesion:
            self.assertEqual(Conversacion.objects.get(id=4).nombre, 'gabriel quiroz') # regresa el nombre concatenado para mostrarte en la lista
        else:
            self.assertEqual(Conversacion.objects.get(id=4).nombre, 'n1 app1 apm1') # regresa el nombre concatenado para mostrarte en la lista
            
            
class GetList200Test(APITestCase):
    def setUp(self):
        Medico.objects.create(nombre='n1', apPaterno='app1', apMaterno='apm1', rfc='rfc1', curp='curp1', fechaNac='2020-09-09', pais='pais1', estado='estado1', ciudad='ciudad1', deleMuni='deleMuni1',
                colonia='colonia', calle='calle1', cp='cp1', numExterior='numExterior1', rfcFacturacion='rfcFacturacion1', cedProfesional='cedProfesional1', cedEspecialidad='cedEspecialidad1',
                cedCirugiaGral='cedCirugiaGral1',hospitalResi='hospitalResi1',telJefEnse='telJefEnse1',fechaInicioResi='1999-06-06',fechaFinResi='2000-07-07',telCelular='telCelular1',
                telParticular='telParticular1',email='email1', numRegistro=333)
        self.json = {
            "mensaje": "mesaje del json",
            "destinatario": 333,
            "remitente": 369
        }
        self.jsonOtro = {
            "mensaje": "mesaje del json",
            "destinatario": 333,
            "remitente": 111
        }
    def test(self):
        self.client.post('/api/chat/create/', data=self.json)
        self.client.post('/api/chat/create/', data=self.json)
        self.client.post('/api/chat/create/', data=self.json)
        self.client.post('/api/chat/create/', data=self.json)
        self.client.post('/api/chat/create/', data=self.json)
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        self.client.post('/api/chat/create/', data=self.jsonOtro)
        
        response = self.client.get('/api/chat/all/369/333/')
        print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')

        response = self.client.get(
            '/api/chat/all/369/333/?size=3&page=1&orderby=id&direc=asc')
        print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')

        response = self.client.get(
            '/api/chat/all/369/333/?size=3&page=2&orderby=id&direc=asc')
        print(f'response JSON ===>>> {nl} {response.json()} {nl} ---')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        