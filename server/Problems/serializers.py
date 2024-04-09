from rest_framework import serializers
from .models import RawProblem, CleanProblem
from Users.models import Usuario

class UserProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'role',
            'dni',
            'ruc',
            'razon_social',
            'phone',
            'address',
            'charge',
            'area',
        ]

class SimpleRawProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawProblem
        fields = '__all__'

class SimpleCleanProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleanProblem
        fields = '__all__'
        
class RawProblemSerializer(serializers.ModelSerializer):
    applicant = UserProblemSerializer(read_only=True)

    class Meta:
        model = RawProblem
        fields='__all__'

class CleanProblemSerializer(serializers.ModelSerializer):
    raw_problem = SimpleRawProblemSerializer(read_only=True)
    class Meta:
        model = CleanProblem
        fields='__all__'