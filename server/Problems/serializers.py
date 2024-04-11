from rest_framework import serializers
from .models import RawProblem
from Users.serializers import NaturalDetailsSerializer
        
class RawProblemSerializer(serializers.ModelSerializer):
    applicant = NaturalDetailsSerializer(read_only=True)

    class Meta:
        model = RawProblem
        fields='__all__'
