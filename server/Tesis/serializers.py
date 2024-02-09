from rest_framework import serializers
from .models import *

class TesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tesis
        fields = '__all__'
    
class ObservacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observaciones
        fields = '__all__'

