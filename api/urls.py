from django.urls import path, re_path
from rest_auth import urls as urls_rest

from .views import *

app_name = 'api'

urlpatterns = [
    # ----------------------------------------------------------------------------------swagger y login
    path('docs/v1.0/', SwaggerSchemaView.as_view(), ),
    path('login/', urls_rest.LoginView.as_view()),   
    
    # path('api-token-auth/', urls_rest.LoginView.as_view()),   
    path('api-token-auth/', CustomAuthToken.as_view()),  
    
    # path('admin/', include('django.contrib.auth.urls')),
    path("password_reset/", password_reset_request, name="password_reset") 
    
]