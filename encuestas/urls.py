from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'encuestas'

urlpatterns = [
    path('create/', EncuestaCreateView.as_view(), ),
    path('list/', EncuestaFilteredListView.as_view(), ),
    path('<pk>/detail/', EncuestaDetailView.as_view(), ),
    path('<pk>/update/', EncuestaUpdateView.as_view(), ),




]