from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
import json
from rest_framework import status
from .models import *


# Create your tests here.
class Post201Test(APITestCase):
    def setUp(self):
        PosicionFront.objects.create(posicion=3, user=9)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        cuenta = PosicionFront.objects.filter(user=9).count()
        print(f'--->>>cuenta: {cuenta}')
        response = self.client.post('/api/front/3/user/9/')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cuenta = PosicionFront.objects.filter(user=9).count()
        print(f'--->>>cuenta: {cuenta}')

        cuenta = PosicionFront.objects.filter(user=9).count()
        print(f'--->>>cuenta: {cuenta}')
        response = self.client.post('/api/front/6/user/9/')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cuenta = PosicionFront.objects.filter(user=9).count()
        print(f'--->>>cuenta: {cuenta}')

        cuenta = PosicionFront.objects.filter(user=9).count()
        print(f'--->>>cuenta: {cuenta}')
        response = self.client.post('/api/front/9/user/9/')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cuenta = PosicionFront.objects.filter(user=9).count()
        print(f'--->>>cuenta: {cuenta}')

        cuenta = PosicionFront.objects.filter(user=9).count()
        print(f'--->>>cuenta: {cuenta}')
        response = self.client.post('/api/front/6/user/6/')
        print(f'response JSON ===>>> \n {json.dumps(response.data)} \n ---')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cuenta = PosicionFront.objects.filter(user=9).count()
        print(f'--->>>cuenta: {cuenta}')


class Get200Test(APITestCase):
    def setUp(self):
        PosicionFront.objects.create(posicion=3, user=9)

        self.user = User.objects.create_user(username='gabriel')  # IsAuthenticated

    def test(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/front/user/9/')
        print(f'response JSON ===>>> \n {json.dumps(response.json())} \n ---')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
