from django.test import TestCase
from .models import *
from datetime import date
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json
from rest_framework import status


def configDB():
    ctde1 = CatTiposDocumentoEntrega.objects.create(descripcion='Certificado1')
    ctde2 = CatTiposDocumentoEntrega.objects.create(descripcion='Certificado2')
    ctde3 = CatTiposDocumentoEntrega.objects.create(descripcion='Certificado3')

    EntregaFisica.objects.create(fecha=date.today(), catTiposDocumentoEntrega=ctde1, nombreRecibe='nombre de quien recibe1', libro=1, foja=1, archivo='ninguno', comentarios='ninguno')


# python manage.py test entregaFisica.tests.BaseDatosTest
class BaseDatosTest(APITestCase):
    def setUp(self):
        configDB()
        self.user = User.objects.create_user(username='gabriel', is_staff=True)  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        datos = EntregaFisica.objects.all()
        for dato in datos:
            print(f'--->>>id: {dato.id} - nombreRecibe: {dato.nombreRecibe} - fecha: {dato.fecha}')
