from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'catalogo'

urlpatterns = [
    path('motivo-rechazo/<textoBusqueda>/', MotivoRechazoListView.as_view(), ),
    
]