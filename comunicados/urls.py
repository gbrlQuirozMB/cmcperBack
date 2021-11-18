from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'comunicados'

urlpatterns = [
    path('create/', ComunicadoCreateView.as_view(), ),
    path('list/', ComunicadoFilteredListView.as_view(), ),
    path('<pk>/detail/', ComunicadoDetailView.as_view(), ),
    path('<pk>/update/', ComunicadoUpdateView.as_view(), ),
    path('<pk>/delete/', ComunicadoDeleteView.as_view(), ),

]
