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
    path('medico/<medicoId>/item/<itemId>/documentos/list/', ItemDocumentosListView.as_view(), ),
    path('documento/create/', ItemDocumentosCreateView.as_view(), ),

    path('medico/<medicoId>/certificados/list/', CertificadosMedicoListView.as_view(), ),
    path('documento/<nombre>/<apPaterno>/<estatus>/list/', ItemDocumentosFilteredListView.as_view(), ),
    path('documento/<pk>/detail/', ItemDocumentosDetailView.as_view(), ),
    path('documento/aceptar/<pk>/', ItemDocumentosAceptar.as_view(), ),
    path('documento/rechazar/<pk>/', ItemDocumentosRechazar.as_view(), ),
    path('documento/reasignar/<pk>/', ItemDocumentosReasignar.as_view(), ),

    path('capitulo/list/', CapituloListView.as_view(), ),
    path('capitulo/<pk>/update/', CapituloUpdateView.as_view(), ),
    path('capitulo/create/', CapituloCreateView.as_view(), ),

    path('subcapitulo/<capituloId>/list/', SubcapituloListView.as_view(), ),
    path('subcapitulo/<pk>/update/', SubcapituloUpdateView.as_view(), ),
    path('subcapitulo/<pk>/detail/', SubcapituloDetailView.as_view(), ),
    path('subcapitulo/create/', SubcapituloCreateView.as_view(), ),

    path('item/<subcapituloId>/list/', ItemListView.as_view(), ),
    path('item/<pk>/update/', ItemUpdateView.as_view(), ),
    path('item/<pk>/detail/', ItemDetailView.as_view(), ),
    path('item/create/', ItemCreateView.as_view(), ),

    path('actualiza-vigencia-certificados/update/', ActualizaVigenciaCertificados.as_view(), ),
    path('solicitud-examen/create/', SolicitudExamenCreateView.as_view(), ),

    path('documento/cedula-especialidad/create/', DocumentoCedulaEspecialidadCreateView.as_view(), ),
    path('documento/certificado/create/', DocumentoCertificadoCreateView.as_view(), ),
    path('documento/foto/create/', DocumentoFotoCreateView.as_view(), ),
    path('documento/carta-solicitud/create/', DocumentoCartaSolicitudCreateView.as_view(), ),

    path('medico/<medicoId>/a-pagar/examen/', PorExamenAPagarEndPoint.as_view(), ),
    path('medico/<medicoId>/a-pagar/renovacion/', RenovacionAPagarEndPoint.as_view(), ),
    path('examen/<pk>/pagado/', PorExamenPagadoUpdateView.as_view(), ),
    path('renovacion/pagado/', RenovacionPagadoCreateView.as_view(), ),

    path('por-examen/list/', PorExamenFilteredListView.as_view(), ),
    path('por-examen/<porExamenId>/documentos/list/', PorExamenDocumentosListView.as_view(), ),
    path('por-examen/documento/aceptar/<pk>/', PorExamenDocumentoAceptarUpdateView.as_view(), ),
    path('por-examen/documento/rechazar/<pk>/', PorExamenDocumentoRechazarUpdateView.as_view(), ),

    path('por-examen/medico/<medicoId>/detail/', PorExamenMedicoDetailView.as_view(), ),

    path('por-examen/fecha/<fechaExamenId>/bajar-excel/list/', PorExamenFechaDownExcel.as_view(), ),
    path('por-examen/fecha/<fechaExamenId>/cargar-excel/update/', PorExamenFechaUpExcel.as_view(), ),
    path('por-examen/fecha/<fechaExamenId>/publicar/list/', PublicarCalificaciones.as_view(), ),

    path('por-examen/<porExamenId>/correo-documentos/', CorreoDocumentosEndPoint.as_view(), ),

    path('fechas-examen/list/', FechasExamenListView.as_view(), ),
    path('fechas-examen/create/', FechasExamenCreateView.as_view(), ),
    path('fechas-examen/<pk>/update/', FechasExamenUpdateView.as_view(), ),

    path('certificado/<pk>/prorroga/<dias>/update/', ProrrogaCertificadoUpdateView.as_view(), ),

    path('renovacion/create/', RenovacionCreateView.as_view(), ),
    path('renovacion/medico/<medicoId>/detail/', RenovacionDetailView.as_view(), ),

    path('documento-qr/create/', QRItemDocumentosCreateView.as_view(), ),
    path('codigo-web/create/', CodigoWEBitemDocumentosCreateView.as_view(), ),

    path('documento-qr/<pk>/update/', QRItemDocumentoUpdateView.as_view(), ),

    path('por-examen/fecha/<fechaExamenId>/list/', PorExamenFechaListView.as_view(), ),
    path('por-examen/<pk>/calificar/', PorExamenFechaCalificarUpdateView.as_view(), ),


]
