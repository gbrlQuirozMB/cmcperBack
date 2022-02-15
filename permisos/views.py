from django.shortcuts import render
from rest_framework.generics import DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from .serializers import *
from api.exceptions import *


class PermisosListView(ListAPIView):
    serializer_class = PermisosListSerializer

    def get_queryset(self):
        queryset = Permission.objects.all().order_by('content_type')
        return queryset
