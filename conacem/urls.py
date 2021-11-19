from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'conacem'

urlpatterns = [
    path('list/', MedicosListView.as_view(), ),
    path('create/', ConacemCreateView.as_view(), ),
    path('bajar-excel/<conacemId>/list/', ConacemDownExcel.as_view(), ),

]
