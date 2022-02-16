from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'permisos'

urlpatterns = [
    path('list/', PermisosListView.as_view(), ),
    path('usuarios/list/', UsuariosFilteredListView.as_view(), ),
    path('usuarios/<pk>/permisos/update/', UsuariosPermisosEndPoint.as_view(), ),
    path('usuarios/<pk>/detail/', UsuariosDetailView.as_view(), ),
    path('usuarios/create/', UsuariosCreateView.as_view(), ),
    path('usuarios/<pk>/update/', UsuariosUpdateView.as_view(), ),
    path('usuarios/<pk>/delete/', UsuariosDeleteView.as_view(), ),
]
