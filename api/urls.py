from django.urls import path, re_path
from rest_auth import urls as urls_rest

from .views import *

app_name = 'api'

urlpatterns = [
    # ----------------------------------------------------------------------------------swagger y login
    # path('docs/v1.0/', SwaggerSchemaView.as_view(), ),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    
    path('login/', urls_rest.LoginView.as_view()),   
    
    # path('api-token-auth/', urls_rest.LoginView.as_view()),   
    path('api-token-auth/', CustomAuthToken.as_view()),  
    
    # path('admin/', include('django.contrib.auth.urls')),
    path("password_reset/", password_reset_request, name="password_reset") 
    
]