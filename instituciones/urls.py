from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

app_name = 'instituciones'

urlpatterns = [
    path('create/', InstitucionCreateView.as_view(), ),
    path('list/', InstitucionFilteredListView.as_view(), ),
    path('<pk>/detail/', InstitucionDetailView.as_view(), ),
    path('<pk>/update/', InstitucionUpdateView.as_view(), ),
    path('<pk>/delete/', InstitucionDeleteView.as_view(), ),



]
