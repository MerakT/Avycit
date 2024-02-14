from dj_rest_auth.serializers import LoginSerializer, TokenSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from .models import Usuario
from Docs.models import FirmaDigital

class CustomTokenSerializer(TokenSerializer):

    class Meta(TokenSerializer.Meta):
        fields = ['key']

class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def get_response_serializer(self):
        return CustomTokenSerializer

    def get_fields(self):
        fields = super(CustomLoginSerializer, self).get_fields()
        fields['email'] = fields['username']
        del fields['username']
        return fields
    
class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)
    nombre = serializers.CharField(required=True)
    apellidos = serializers.CharField(required=True)
    role = serializers.CharField(required=True)

    class Meta:
        model = Usuario

    def custom_signup(self, request, user):
        user.username = self.validated_data.get('email', '')
        user.first_name = self.validated_data.get('nombre', '')
        user.last_name = self.validated_data.get('apellidos', '')
        user.phone = self.validated_data.get('telefono', '')
        user.role = self.validated_data.get('role', '')
        user.save()
        return super().custom_signup(request, user)
    
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'role']