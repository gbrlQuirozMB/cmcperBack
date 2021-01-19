from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'notificaciones'

urlpatterns = [
    # ----------------------------------------------------------------------------------Chat
    # path('comprar-carta/', csrf_exempt(CarritoCreateView.as_view()), ),
    path('all/<int:destinatario>/', NotificacionListEndPoint.as_view(), ),
    
]