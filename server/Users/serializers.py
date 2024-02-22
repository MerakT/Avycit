from dj_rest_auth.serializers import LoginSerializer, TokenSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from .models import Usuario
from Docs.models import FirmaDigital

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        exclude = (
            'password', 
            'is_superuser', 
            'is_staff', 
            'is_active', 
            'date_joined', 
            'last_login', 
            'groups',
            'user_permissions',
            'registration_method',
        )

class CustomTokenSerializer(TokenSerializer):

    # Get the User data to pass to the response
    user = serializers.SerializerMethodField(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ['key', 'user']
        
    def get_user(self, obj):
        # Use the CustomUserDetailsSerializer to serialize the user data
        user_serializer = UserSerializer(obj.user)
        return user_serializer.data

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
        # General Data
        if self.validated_data.get('username', ''):
            user.username = self.validated_data.get('username', '')
        else:
            user.username = self.validated_data.get('email', '')
        user.email = self.validated_data.get('email', '')
        user.first_name = self.validated_data.get('nombre', '')
        user.last_name = self.validated_data.get('apellidos', '')
        user.role = self.validated_data.get('role', '')

        # UDH Data
        user.career = self.validated_data.get('career', None)
        user.code = self.validated_data.get('code', None)
        user.grado = self.validated_data.get('grado', None)
        user.signature_photo = self.validated_data.get('signature_photo', None)

        # Banco de Problemas Data
        user.dni = self.validated_data.get('dni', None)
        user.ruc = self.validated_data.get('ruc', None) # EMPRESA
        user.razon_social = self.validated_data.get('razon_social', None) # EMPRESA
        user.phone = self.validated_data.get('phone', None)
        user.address = self.validated_data.get('address', None)
        user.can_finance = self.validated_data.get('can_finance', None)
        user.charge = self.validated_data.get('charge', None) # EMPRESA
        user.area = self.validated_data.get('area', None) # EMPRESA

        # Save the User
        user.save()
        return super().custom_signup(request, user)
    