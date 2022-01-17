"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/preregistro/', include('preregistro.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/notificaciones/', include('notificaciones.urls')),
    path('api/convocatoria/', include('convocatoria.urls')),
    path('api/catalogo/', include('catalogos.urls')),
    path('api/front/', include('front.urls')),
    path('api/recertificacion/', include('recertificacion.urls')),
    path('api/tesoreria/', include('tesoreria.urls')),
    path('api/certificados/', include('certificados.urls')),
    path('api/comunicados/', include('comunicados.urls')),
    path('api/instituciones/', include('instituciones.urls')),
    path('api/actividades-avaladas/', include('actividadesAvaladas.urls')),
    path('api/facturacion/', include('facturacion.urls')),
    path('api/reportes/', include('reportes.urls')),
    path('api/conacem/', include('conacem.urls')),
    path('api/entrega-fisica/', include('entregaFisica.urls')),

    path('api/admin/password_reset/', auth_views.PasswordResetView.as_view(template_name='admin/password_reset.html'), name='password_reset'),
    path('api/admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='admin/password_reset_done.html'), name='password_reset_done'),
    path('api/admin/password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='admin/password_reset_confirm.html'), name='password_reset_confirm'),
    path('api/admin/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='admin/password_reset_complete.html'), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
