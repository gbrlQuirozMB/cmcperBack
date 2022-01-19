from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'entrega-fisica'

urlpatterns = [
    path('create/', EntregaFisicaCreateView.as_view(), ),
    path('list/', EntregaFisicaFilteredListView.as_view(), ),
    path('<pk>/detail/', EntregaFisicaDetailView.as_view(), ),
    path('<pk>/update/', EntregaFisicaUpdateView.as_view(), ),
    path('<pk>/delete/', EntregaFisicaDeleteView.as_view(), ),

    path('tipo-documento/create/', CatTiposDocumentoEntregaCreateView.as_view(), ),
    path('tipo-documento/list/', CatTiposDocumentoEntregaListView.as_view(), ),
    path('tipo-documento/<pk>/detail/', CatTiposDocumentoEntregaDetailView.as_view(), ),
    path('tipo-documento/<pk>/update/', CatTiposDocumentoEntregaUpdateView.as_view(), ),

]
