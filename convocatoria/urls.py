from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'convocatoria'

urlpatterns = [
    path('medico/es-extranjero/<pk>/', EsExtranjeroUpdateView.as_view(), ),
    path('medico/estudio-extranjero/<pk>/', EstudioExtranjeroUpdateView.as_view(), ),

    path('create/', ConvocatoriaCreateView.as_view(), ),
    path('list/', ConvocatoriaListView.as_view(), ),
    path('detail/<pk>/', ConvocatoriaDetailView.as_view(), ),
    path('<pk>/archivo/', ConvocatoriaArchivoUpdateView.as_view(), ),
    path('<pk>/banner/', ConvocatoriaBannerUpdateView.as_view(), ),
    path('update/<pk>/', ConvocatoriaUpdateView.as_view(), ),
    path('delete/<pk>/', ConvocatoriaDeleteView.as_view(), ),

    path('enrolar/create/', ConvocatoriaEnroladoCreateView.as_view(), ),
    path('enrolar/medico/<medicoId>/detail/', ConvocatoriaEnroladoMedicoDetailView.as_view(), ),
    path('<convocatoriaId>/enrolados/<isAceptado>/<nombre>/<apPaterno>/list/', ConvocatoriaEnroladosMedicoListView.as_view(), ),  # normal
    # path('<convocatoriaId>/enrolados/<isAceptado>/<nombre>/<apPaterno>/list/', ConvocatoriaEnroladosMedicoEndPoint.as_view(), ), # paginado
    path('enrolar/comentario/update/<pk>/', ConvocatoriaEnroladoComentarioUpdateView.as_view(), ),

    path('documento/revalidacion/create/', DocumentoRevalidacionCreateView.as_view(), ),
    path('documento/curp/create/', DocumentoCurpCreateView.as_view(), ),
    path('documento/acta-nacimiento/create/', DocumentoActaNacimientoCreateView.as_view(), ),
    path('documento/carta-solicitud/create/', DocumentoCartaSolicitudCreateView.as_view(), ),
    path('documento/constancia-posgrado/create/', DocumentoConstanciaPosgradoCreateView.as_view(), ),
    path('documento/cedula-especialidad/create/', DocumentoCedulaEspecialidadCreateView.as_view(), ),
    path('documento/titulo-licenciatura/create/', DocumentoTituloLicenciaturaCreateView.as_view(), ),
    path('documento/cedula-profesional/create/', DocumentoCedulaProfesionalCreateView.as_view(), ),
    path('documento/constancia-cirugia/create/', DocumentoConstanciaCirugiaCreateView.as_view(), ),
    path('documento/carta-profesor/create/', DocumentoCartaProfesorCreateView.as_view(), ),
    # path('documentos/medico/<medicoId>/list/', DocumentosMedicoListView.as_view(), ), # se va a cambiar por la siguiente
    path('<convocatoriaId>/medico/<medicoId>/documentos/list/', DocumentosMedicoListView.as_view(), ),
    path('documento/update/<pk>/', ConvocatoriaDocumentoUpdateView.as_view(), ),
    path('documento/aceptar/<pk>/', ConvocatoriaEnroladoDocumentoAceptarUpdateView.as_view(), ),
    path('documento/rechazar/<pk>/', ConvocatoriaEnroladoDocumentoRechazarUpdateView.as_view(), ),
    path('engargolado/aceptar/<pk>/', ConvocatoriaEnroladoEngargoladoAceptarUpdateView.as_view(), ),
    path('engargolado/rechazar/<pk>/', ConvocatoriaEnroladoEngargoladoRechazarUpdateView.as_view(), ),

    path('ficha-registro-pdf/<pk>/', FichaRegistroPDF.as_view(), ),
    path('<convocatoriaId>/medico/<medicoId>/a-pagar/', ConvocatoriaEnroladoMedicoAPagarEndPoint.as_view(), ),
    path('enrolar/<pk>/pagado/', ConvocatoriaEnroladoMedicoPagadoUpdateView.as_view(), ),



    # ES DE PRUEBA NO USAR!!!
    # path('<convocatoriaId>/sede/create/', ConvocatoriaSedeCreateView.as_view(), ),


]
