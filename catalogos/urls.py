from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'catalogo'

urlpatterns = [
    path('motivo-rechazo/list/<textoBusqueda>/', CatMotivoRechazoListView.as_view(), ),
    path('motivo-rechazo/create/', CatMotivosRechazoCreateView.as_view(), ),
    path('motivo-rechazo/<pk>/update/', CatMotivosRechazoUpdateView.as_view(), ),
    path('motivo-rechazo/<pk>/delete/', CatMotivosRechazoDeleteView.as_view(), ),

    path('pagos/create/', CatPagosCreateView.as_view(), ),
    path('pagos/list/', CatPagosFilteredListView.as_view(), ),
    path('pagos/<pk>/update/', CatPagosUpdateView.as_view(), ),


]
