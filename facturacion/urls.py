from django.urls import path
from .views import *

app_name = 'facturacion'

urlpatterns = [
    path('metodo-pago/list/', MetodoPagoListView.as_view()),
    path('conceptoPago/list/', ConceptoPagoListView.as_view()),
    path('moneda/list/', MonedaListView.as_view()),
    path('formaPago/list/', FormaPagoListView.as_view()),
    path('usoCFDI/list/', UsoCFDIListView.as_view()),
    path('aval/list/', AvalFilteredListView.as_view()),  # Aval se refiere al modelo de Institucion
    path('medico/list/', MedicoFilteredListView.as_view()),
    path('factura/idUltimaFactura/', IdUltimaFacturaView.as_view()),
    path('pais/list/', PaisListView.as_view()),
    path('create/', FacturaCreateView.as_view()),
    path('list/', FacturaFilteredListView.as_view()),
    path('cancelar/', FacturaCancelarView.as_view()),

    path('bajar-excel/list/', FacturaFilteredDownExcelListView.as_view()),

    path('concepto-pago/create/', ConceptoPagoCreateView.as_view()),
    path('concepto-pago/<pk>/update/', ConceptoPagoUpdateView.as_view()),

    path('forma-pago/create/', FormaPagoCreateView.as_view()),
    path('forma-pago/<pk>/update/', FormaPagoUpdateView.as_view()),

]
