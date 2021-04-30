from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'certificados'

urlpatterns = [
    path('list/', CertificadosFilteredListView.as_view(), ),
    path('<pk>/subir-documento/update/', CertificadoSubirDocumentoUpdateView.as_view(), ),

]
