from rest_framework import serializers
from .models import *
from Users.serializers import StudentDetailsSerializer, CuratorDetailsSerializer
from Problems.models import RawProblem

#------------------------------------- PropuestaTesis RELATED -------------------------------------
class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

class CausasSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Causas

class ConsecuenciasSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Consecuencias

class AportesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Aportes

class VariablesSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = Variables

class ObjetivosEspSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = ObjetivosEsp

class HipotesisEspSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = HipotesisEsp

#------------------------------------- SIMPLE SERIALIZER ( NO RELATIONSHIPS ) -------------------------------------
class SimpleRawProblemSerializer(BaseSerializer):
    class Meta(BaseSerializer.Meta):
        model = RawProblem

class SimplePropuestaTesisSerializer(serializers.ModelSerializer):
    creator = StudentDetailsSerializer(read_only=True)
    career = serializers.SlugRelatedField(slug_field='name', queryset=ProgAcad.objects.all())
    propuesta_raw = SimpleRawProblemSerializer(read_only=True)
    class Meta:
        model = PropuestaTesis
        fields = '__all__'

#------------------------------------- COMPLEX SERIALIZER ( WITH RELATIONSHIPS ) -------------------------------------
class PostulacionesSerializer(serializers.ModelSerializer):
    tesista = StudentDetailsSerializer(read_only=True)
    propuesta = SimplePropuestaTesisSerializer(read_only=True)
    class Meta:
        model = Postulaciones
        fields = '__all__'

class PropuestaTesisSerializer(serializers.ModelSerializer):
    creator = CuratorDetailsSerializer(read_only=True)
    career = serializers.SlugRelatedField(slug_field='name', queryset=ProgAcad.objects.all())
    propuesta_raw = SimpleRawProblemSerializer(read_only=True)
    postulaciones = serializers.SerializerMethodField('get_postulaciones_data')
    causas = CausasSerializer(many=True)
    consecuencias = ConsecuenciasSerializer(many=True)
    aportes = AportesSerializer(many=True)
    variables = VariablesSerializer(many=True)
    objetivos = ObjetivosEspSerializer(many=True)
    hipotesis = HipotesisEspSerializer(many=True)

    def get_postulaciones_data(self, obj):
        try:
            postulaciones = Postulaciones.objects.filter(propuesta=obj)
            return PostulacionesSerializer(postulaciones, many=True).data
        except:
            return []

    def create(self, validated_data):
        causas_data = validated_data.pop('causas')
        consecuencias_data = validated_data.pop('consecuencias')
        aportes_data = validated_data.pop('aportes')
        variables_data = validated_data.pop('variables')
        objetivos_data = validated_data.pop('objetivos')
        hipotesis_data = validated_data.pop('hipotesis')

        propuesta_tesis = PropuestaTesis.objects.create(**validated_data)

        Causas.objects.bulk_create([
            Causas(propuesta=propuesta_tesis, **data) 
            for data in causas_data
        ])
        Consecuencias.objects.bulk_create([
            Consecuencias(propuesta=propuesta_tesis, **data) 
            for data in consecuencias_data
        ])
        Aportes.objects.bulk_create([
            Aportes(propuesta=propuesta_tesis, **data) 
            for data in aportes_data
        ])
        Variables.objects.bulk_create([
            Variables(propuesta=propuesta_tesis, **data) 
            for data in variables_data
        ])
        ObjetivosEsp.objects.bulk_create([
            ObjetivosEsp(propuesta=propuesta_tesis, **data) 
            for data in objetivos_data
        ])
        HipotesisEsp.objects.bulk_create([
            HipotesisEsp(propuesta=propuesta_tesis, **data) 
            for data in hipotesis_data
        ])
        return propuesta_tesis
    
    class Meta:
        model = PropuestaTesis
        fields = '__all__'

#------------------------------------- Tesis RELATED -------------------------------------
class TesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tesis
        fields = '__all__'
    
class ObservacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observaciones
        fields = '__all__'

