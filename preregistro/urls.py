from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'preregistro'

urlpatterns = [
    # ----------------------------------------------------------------------------------Carta
    # path('comprar-carta/', csrf_exempt(CarritoCreateView.as_view()), ),
    path('create/', PreregistroCreateView.as_view(), ),
]
