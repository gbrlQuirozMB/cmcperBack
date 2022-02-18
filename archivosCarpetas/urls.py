from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'archivos-carpetas'

urlpatterns = [
    path('carpeta/create/', CarpetaCreateView.as_view(), ),
    path('carpeta/list/', CarpetaListView.as_view(), ),
    path('carpeta/<pk>/detail/', CarpetaDetailView.as_view(), ),
    path('carpeta/<pk>/update/', CarpetaUpdateView.as_view(), ),
    path('carpeta/<pk>/delete/', CarpetaDeleteView.as_view(), ),

    path('archivo/create/', ArchivoCreateView.as_view(), ),
    path('archivo/list/', ArchivoFilteredListView.as_view(), ),
    path('archivo/<pk>/detail/', ArchivoDetailView.as_view(), ),
]
