from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'preregistro'

urlpatterns = [
    # ----------------------------------------------------------------------------------Preregistro
    # path('comprar-carta/', csrf_exempt(CarritoCreateView.as_view()), ),
    path('create/', PreregistroCreateView.as_view(), ),
    path('list/', PreregistroListEndPoint.as_view(), ),
    path('detail/<pk>/', PreregistroDetailView.as_view(), ),
    path('aceptar/<pk>/', PreregistroAceptadoUpdateView.as_view(), ),
    path('rechazar/<pk>/', PreregistroRechazadoUpdateView.as_view(), ),
    path('medico/<pk>/foto-perfil/', FotoPerfilUpdateView.as_view(), ),

    path('horario-atencion/create/', HorarioAtencionCreateView.as_view(), ),
    path('horario-atencion/medico/<medicoId>/list/', HorarioAtencionListView.as_view(), ),
    path('horario-atencion/<pk>/detail/', HorarioAtencionDetailView.as_view(), ),


]
