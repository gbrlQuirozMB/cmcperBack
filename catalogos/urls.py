from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'catalogo'

urlpatterns = [
    path('motivo-rechazo/<textoBusqueda>/', MotivoRechazoListView.as_view(), ),

    path('pagos/create/', CatPagosCreateView.as_view(), ),
    path('pagos/list/', CatPagosFilteredListView.as_view(), ),
    path('pagos/<pk>/update/', CatPagosUpdateView.as_view(), ),


]
