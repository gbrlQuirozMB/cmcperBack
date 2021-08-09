from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'reportes'

urlpatterns = [
    path('med-residentes/list/', MedResidenteFilteredListView.as_view(), ),

]
