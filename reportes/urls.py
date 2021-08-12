from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'reportes'

urlpatterns = [
    path('med-residentes/list/', MedResidenteFilteredListView.as_view(), ),
    path('med-residentes/<pk>/detail/', MedResidenteDetailView.as_view(), ),
    path('med-residentes/<medicoId>/extras/', MedResidenteExtrasDetailView.as_view(), ),

    path('med-certificados/list/', MedCertificadoFilteredListView.as_view(), ),
    path('med-certificados/<pk>/detail/', MedCertificadoDetailView.as_view(), ),


]
