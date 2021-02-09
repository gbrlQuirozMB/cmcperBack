from preregistro.models import Medico
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
        if user.is_superuser:
            idMedico = 'No es medico'
        else:
            datoMedico = Medico.objects.filter(username=user).values_list('id')
            idMedico = datoMedico[0][0]
        
        return Response({
            'token': token.key,
            'idUser': user.pk,
            'idMedico': idMedico,
            'email': user.email,
            'firstName': user.first_name,
            'lastName': user.last_name,
            'isSuperuser': user.is_superuser,
            'permisos': user.get_user_permissions()
            # permisos en version django 2.2
            # 'permisos': permissions
        })
