from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'convocatoria'

urlpatterns = [
    # ----------------------------------------------------------------------------------Preregistro
    path('medico/es-extranjero/<pk>/', EsExtranjeroUpdateView.as_view(), ),
    path('medico/estudio-extranjero/<pk>/', EstudioExtranjeroUpdateView.as_view(), ),
    path('create/', ConvocatoriaCreateView.as_view(), ),
    
]
