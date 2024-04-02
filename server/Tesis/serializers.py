from rest_framework import serializers
from .models import *
from Users.models import Usuario
from Problems.models import RawProblem

class UserThesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'code',
            'career',
            'grado',
            'role',
            'dni',
        ]

class SimpleRawProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawProblem
        fields = '__all__'

class PostulacionesSerializer(serializers.ModelSerializer):
    tesista = UserThesisSerializer(read_only=True)
    class Meta:
        model = Postulaciones
        fields = '__all__'

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

class PropuestaTesisSerializer(serializers.ModelSerializer):
    propuesta_raw = SimpleRawProblemSerializer(read_only=True)
    postulaciones = PostulacionesSerializer(many=True)
    causas = CausasSerializer(many=True)
    consecuencias = ConsecuenciasSerializer(many=True)
    aportes = AportesSerializer(many=True)
    variables = VariablesSerializer(many=True)
    objetivos = ObjetivosEspSerializer(many=True)
    hipotesis = HipotesisEspSerializer(many=True)

    def create(self, validated_data):
        postulaciones_data = validated_data.pop('postulaciones')
        causas_data = validated_data.pop('causas')
        consecuencias_data = validated_data.pop('consecuencias')
        aportes_data = validated_data.pop('aportes')
        variables_data = validated_data.pop('variables')
        objetivos_data = validated_data.pop('objetivos')
        hipotesis_data = validated_data.pop('hipotesis')

        propuesta_tesis = PropuestaTesis.objects.create(**validated_data)

        Postulaciones.objects.bulk_create([
            Postulaciones(propuesta=propuesta_tesis, **data) 
            for data in postulaciones_data
        ])
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

class TesisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tesis
        fields = '__all__'
    
class ObservacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observaciones
        fields = '__all__'

