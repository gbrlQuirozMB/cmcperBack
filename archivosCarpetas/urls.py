from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'archivos-carpetas'

urlpatterns = [
    path('carpeta/create/', CarpetaCreateView.as_view(), ),
    path('carpeta/list/', CarpetaListView.as_view(), ),

]
