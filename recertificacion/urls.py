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
    path('documento/create/', ItemDocumentosCreateView.as_view(), ),

    path('medico/<medicoId>/certificados/list/', CertificadosMedicoListView.as_view(), ),
    path('<nombre>/<apPaterno>/<estatus>/list/', ItemDocumentosFilteredListView.as_view(), ),
    path('documento/<pk>/detail/', ItemDocumentosDetailView.as_view(), ),
    path('documento/aceptar/<pk>/', ItemDocumentosAceptar.as_view(), ),
    path('documento/rechazar/<pk>/', ItemDocumentosRechazar.as_view(), ),
    path('documento/reasignar/<pk>/', ItemDocumentosReasignar.as_view(), ),
    path('capitulo/list/', CapituloListView.as_view(), ),
    path('subcapitulo/<capituloId>/list/', SubcapituloListView.as_view(), ),
    path('item/<subcapituloId>/list/', ItemListView.as_view(), ),

    path('actualiza-vigencia-certificados/update/', ActualizaVigenciaCertificados.as_view(), ),
    path('solicitud-examen/create/', SolicitudExamenCreateView.as_view(), ),

    path('documento/cedula-especialidad/create/', DocumentoCedulaEspecialidadCreateView.as_view(), ),
    path('documento/certificado/create/', DocumentoCertificadoCreateView.as_view(), ),

    path('medico/<medicoId>/a-pagar/examen/', PorExamenAPagarEndPoint.as_view(), ),
    path('medico/<medicoId>/a-pagar/renovacion/', RenovacionAPagarEndPoint.as_view(), ),





]
