from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'chat'

urlpatterns = [
    # ----------------------------------------------------------------------------------Chat
    # path('comprar-carta/', csrf_exempt(CarritoCreateView.as_view()), ),
    path('create/', ChatCreateView.as_view(), ),
    
    
]