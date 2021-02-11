from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'convocatoria'

urlpatterns = [
    # ----------------------------------------------------------------------------------Preregistro
    path('medico/es-extranjero/<pk>/', esExtranjeroUpdateView.as_view(), ),
    
]
