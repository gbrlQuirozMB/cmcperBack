from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'encuestas'

urlpatterns = [
    path('create/', EncuestaCreateView.as_view(), ),
    path('list/', EncuestaFilteredListView.as_view(), ),
    path('<pk>/detail/', EncuestaDetailView.as_view(), ),
    path('<pk>/update/', EncuestaUpdateView.as_view(), ),
    path('<pk>/delete/', EncuestaDeleteView.as_view(), ),

    path('<pk>/preguntas/create/', PreguntaCreateView.as_view(), ),
    path('<pk>/preguntas/list/', PreguntaListView.as_view(), ),
    path('preguntas/<pk>/detail/', PreguntaDetailView.as_view(), ),
    path('preguntas/<pk>/update/', PreguntaUpdateView.as_view(), ),
    path('preguntas/<pk>/delete/', PreguntaDeleteView.as_view(), ),

    path('preguntas/<pk>/opciones/create/', OpcionCreateView.as_view(), ),
    path('preguntas/<pk>/opciones/list/', OpcionListView.as_view(), ),
    path('preguntas/opciones/<pk>/detail/', OpcionDetailView.as_view(), ),
    path('preguntas/opciones/<pk>/update/', OpcionUpdateView.as_view(), ),
    path('preguntas/opciones/<pk>/delete/', OpcionDeleteView.as_view(), ),

    path('respuestas/create/', RespuestaCreateView.as_view(), ),
    path('respuestas/list/', RespuestaFilteredListView.as_view(), ),


]
