from dj_rest_auth.serializers import LoginSerializer, TokenSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.db import transaction

from .models import Usuario, ProgAcad, ROLE_CHOICES


class CustomTokenSerializer(TokenSerializer):

    # Get the User data to pass to the response
    user = serializers.SerializerMethodField(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ['key', 'user']
        
    def get_user(self, obj):
        # Use the UserDetailsSerializer to serialize the user data
        user_serializer = UserDetailsSerializer(obj.user)
        return user_serializer.data

class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def get_response_serializer(self):
        return CustomTokenSerializer
    
    def get_fields(self):
        fields = super().get_fields()
        fields['email'] = fields['username']
        del fields['username']
        return fields
    
class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)
    nombre = serializers.CharField(required=True)
    apellidos = serializers.CharField(required=True)

    class Meta:
        model = Usuario

    def validate(self, data):
        data = super().validate(data)

        # Check if the role is valid
        role = data.get('role')
        if not role or role not in ROLE_CHOICES:
            raise serializers.ValidationError({'role': 'Invalid or missing role'})

        return data

    @transaction.atomic
    def custom_signup(self, request, user):
        # General Data
        user.username = self.validated_data.get('email')
        user.email = self.validated_data.get('email')
        user.first_name = self.validated_data.get('nombre')
        user.last_name = self.validated_data.get('apellidos')
        user.role = self.validated_data.get('role')

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
    
class UserDetailsSerializer(serializers.ModelSerializer):
    # Get the signature photo URL
    signature_photo = serializers.ImageField(use_url=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 
            'email', 
            'first_name', 
            'last_name', 
            'role', 
            'career', 
            'code', 
            'grado', 
            'signature_photo', 
            'dni', 
            'ruc', 
            'razon_social', 
            'phone', 
            'address', 
            'can_finance', 
            'charge', 
            'area'
        ]
        read_only_fields = ['id', 'email', 'role', 'career', 'code']

class ProgAcadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgAcad
        fields = ['id', 'name']