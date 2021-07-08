from django.urls import path
from .views import *

app_name = 'facturacion'

urlpatterns = [
    path('conceptoPago/list/', ConceptoPagoListView.as_view()),
    path('moneda/list/', MonedaListView.as_view()),
    path('formaPago/list/', FormaPagoListView.as_view()),
    path('usoCFDI/list/', UsoCFDIListView.as_view()),
    path('aval/list/', AvalListView.as_view()),#Aval se refiere al modelo de Institucion
]