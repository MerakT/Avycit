from rest_framework import serializers
from .models import RawProblem, CleanProblem

class RawProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawProblem
        fields='__all__'

class CleanProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleanProblem
        fields='__all__'