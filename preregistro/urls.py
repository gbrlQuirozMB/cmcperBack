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
    path('update/<pk>/', PreregistroUpdateView.as_view(), ),

    path('horario-atencion/create/', HorarioAtencionCreateView.as_view(), ),
    path('horario-atencion/medico/<medicoId>/list/', HorarioAtencionListView.as_view(), ),
    path('horario-atencion/<pk>/detail/', HorarioAtencionDetailView.as_view(), ),
    path('horario-atencion/<pk>/update/', HorarioAtencionUpdateView.as_view(), ),
    path('horario-atencion/<pk>/delete/', HorarioAtencionDeleteView.as_view(), ),
    
    path('notas-observaciones/create/', NotasObservacionesCreateView.as_view(), ),
    path('notas-observaciones/list/', NotasObservacionesFilteredListView.as_view(), ),
    
    
    # path('genera-usuarios-pass/', UsuariosPassEndPoint.as_view(), ),
    
    


]
