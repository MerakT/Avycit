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
        if self.validated_data.get('username', ''):
            user.username = self.validated_data.get('username', '')
        else:
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
        fields = ['first_name', 'last_name', 'phone']