from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'actividades-avaladas'

urlpatterns = [
    path('create/', ActividadAvaladaCreateView.as_view(), ),
    path('<pk>/archivo/', ActividadAvaladaArchivoUpdateView.as_view(), ),
    path('<pk>/banner/', ActividadAvaladaBannerUpdateView.as_view(), ),
    path('list/', ActividadAvaladaFilteredListView.as_view(), ),
    path('<pk>/detail/', ActividadAvaladaDetailView.as_view(), ),
    path('<pk>/update/', ActividadAvaladaUpdateView.as_view(), ),
    path('<pk>/delete/', ActividadAvaladaDeleteView.as_view(), ),
    path('<pk>/pagado/', ActividadAvaladaPagadoView.as_view(), ),


    path('asistente/create/', AsistenteActividadAvaladaCreateView.as_view(), ),
    path('<pk>/asistentes/cupos/', CuposAsistentesDetailView.as_view(), ),
    path('medicos/list/', MedicosAIncribirseAAFilteredListView.as_view(), ),
    path('asistentes/list/', MedicosAsistenteAAFilteredListView.as_view(), ),
    path('asistente/<pk>/delete/', MedicosAsistenteAADeleteView.as_view(), ),

]
