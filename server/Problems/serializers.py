from rest_framework import serializers
from .models import RawProblem, CleanProblem
from Users.serializers import NaturalDetailsSerializer
        
class RawProblemSerializer(serializers.ModelSerializer):
    applicant = NaturalDetailsSerializer(read_only=True)

    class Meta:
        model = RawProblem
        fields='__all__'

class CleanProblemSerializer(serializers.ModelSerializer):
    creator = NaturalDetailsSerializer(read_only=True)
    class Meta:
        model = CleanProblem
        fields='__all__'
