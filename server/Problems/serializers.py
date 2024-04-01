from rest_framework import serializers
from .models import RawProblem, CleanProblem
from Users.models import Usuario
from Tesis.models import Postulaciones
from Tesis.serializers import SimplePostulacionesSerializer

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
    clean_data = serializers.SerializerMethodField()
    postulations = serializers.SerializerMethodField()

    def get_clean_data(self, obj):
        try:
            clean_problem = CleanProblem.objects.get(raw_problem=obj.id)
            if not clean_problem:
                return None
            return SimpleCleanProblemSerializer(clean_problem).data
        except CleanProblem.DoesNotExist:
            return None
        
    def get_postulations(self, obj):
        postulations = Postulaciones.objects.filter(problem=obj.id)
        if not postulations:
            return None
        return SimplePostulacionesSerializer(postulations, many=True).data

    class Meta:
        model = RawProblem
        fields='__all__'

class CleanProblemSerializer(serializers.ModelSerializer):
    raw_problem = SimpleRawProblemSerializer(read_only=True)
    class Meta:
        model = CleanProblem
        fields='__all__'