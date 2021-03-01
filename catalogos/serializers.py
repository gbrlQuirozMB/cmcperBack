from .models import *
from rest_framework import fields, serializers
from api.logger import log
from api.exceptions import *

class CatMotivosRechazoSerializer(serializers.ModelSerializer):
    tipo = serializers.CharField(source='get_tipo_display')
    
    class Meta:
        model = CatMotivosRechazo
        fields = '__all__'