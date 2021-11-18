from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'tesoreria'

urlpatterns = [
    path('subir-pago/create/', SubirPagoCreateView.as_view(), ),
    path('pagos/<int:estatus>/list/', PagosListView.as_view(), ),
    path('pago/aceptar/<pk>/', PagoAceptarUpdateView.as_view(), ),
    path('pago/rechazar/<pk>/', PagoRechazarUpdateView.as_view(), ),
    
    path('pago/list/', PagoFilteredListView.as_view(), ),
        
]