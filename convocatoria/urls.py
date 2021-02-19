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
    path('enrolar/create/', ConvocatoriaEnroladoCreateView.as_view(), ),
    path('documento/revalidacion/create/', DocumentoRevalidacionCreateView.as_view(), ),
    path('documento/curp/create/', DocumentoCurpCreateView.as_view(), ),
    path('documento/acta-nacimiento/create/', DocumentoActaNacimientoCreateView.as_view(), ),
    path('documento/carta-solicitud/create/', DocumentoCartaSolicitudCreateView.as_view(), ),
    
]
