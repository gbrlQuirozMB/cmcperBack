from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'front'

urlpatterns = [
    # path('<posicion>/user/<user>/', PosicionFrontPostEndPoint.as_view(), ),
    path('<posicion>/user/<userId>/', PosicionFrontCreateView.as_view(), ),
    path('user/<userId>/', PosicionFrontDetailView.as_view(), ),

]
