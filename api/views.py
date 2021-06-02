from preregistro.models import Medico
from instituciones.models import Institucion

from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework_swagger import renderers
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
# Create your views here.
from django.contrib.auth.models import Permission


from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from django.contrib.sites.shortcuts import get_current_site

from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


class SwaggerSchemaView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator(title='CMCPER API')
        schema = generator.get_schema(request=request, public=True)

        return Response(schema)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # permisos en version django 2.2
        # permissions = Permission.objects.filter(user=request.user)
        # permissions = Permission.objects.filter(user=user).values_list('name', flat=True)
        if user.is_superuser or user.is_staff:
            idMedico = 'No es medico'
            datoInsti = Institucion.objects.filter(username=user).values_list('id')
            if datoInsti:
                idInsti = datoInsti[0][0]
            else:
                idInsti = 'No es una institución'
        else:
            datoMedico = Medico.objects.filter(username=user).values_list('id')
            idMedico = datoMedico[0][0]
            idInsti = 'No es una institución'

        return Response({
            'token': token.key,
            'idUser': user.pk,
            'idMedico': idMedico,
            'idInstitucion': idInsti,
            'email': user.email,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'isSuperuser': user.is_superuser,
            'permisos': user.get_user_permissions()
            # permisos en version django 2.2
            # 'permisos': permissions
        })


# class MyPasswordResetForm(PasswordResetForm):
# 	field_order = ['email']


def password_reset_request(request):
    if request.method == 'POST':
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = 'CMCPER - Solicitud de cambio de contraseña'
                    email_template_name = 'admin/password_reset_email.html'
                    current_site = get_current_site(request)
                    datos = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'],
                        # 'site_name': current_site.name,
                        # 'domain_dos': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    try:
                        htmlContent = render_to_string(email_template_name, datos)
                        textContent = strip_tags(htmlContent)
                        emailAcep = EmailMultiAlternatives(subject, textContent, "no-reply@cmcper.mx", [user.email])
                        emailAcep.attach_alternative(htmlContent, "text/html")
                        emailAcep.send()
                    except BadHeaderError:
                        return HttpResponse('Header incorrecto')
                    return redirect('/api/admin/password_reset/done/')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name='admin/password_reset.html', context={'password_reset_form': password_reset_form})
