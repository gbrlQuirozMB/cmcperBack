from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'permisos'

urlpatterns = [
    path('list/', PermisosListView.as_view(), ),
]
