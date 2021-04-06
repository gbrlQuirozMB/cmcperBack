from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'recertificacion'

urlpatterns = [
    path('medico/<medicoId>/', CertificadoDatosDetailView.as_view(), ),
    
    
]
    