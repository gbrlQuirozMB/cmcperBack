from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'permisos'

urlpatterns = [
    path('list/', PermisosListView.as_view(), ),
    path('usuarios/list/', UsuariosFilteredListView.as_view(), ),
    path('usuarios/<pk>/permisos/update/', UsuariosPermisosEndPoint.as_view(), ),
]
