from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'recertificacion'

urlpatterns = [
    path('medico/<medicoId>/', CertificadoDatosDetailView.as_view(), ),
    path('medico/<medicoId>/capitulo/<capituloId>/avance/', AvanceMedicoCapituloDetailView.as_view(), ),
    path('puntos-capitulo/list/', PuntosCapituloListView.as_view(), ),
    path('puntos-capitulo/<pk>/detail/', PuntosCapituloDetailView.as_view(), ),
    path('porcentaje/medico/<medicoId>/', PorcentajeGeneralMedicoDetailView.as_view(), ),
    path('puntos/capitulo/<capituloId>/medico/<medicoId>/', PuntosPorCapituloMedicoDetailView.as_view(), ),
    path('capitulo/<pk>/detail/', DetallesCapituloDetailView.as_view(), ),
    path('item/<itemId>/documentos/list/', ItemDocumentosListView.as_view(), ),


]
