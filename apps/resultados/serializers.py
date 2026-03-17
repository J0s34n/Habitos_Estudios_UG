from rest_framework import serializers
from .models import Resultado, RespuestaDetalle

class EnviarRespuestaSeriallizer(serializers.Serializer):
    test_id = serializers.IntegerField()
    # Lista de {pregunta_id, opcion_id}
    respuestas = serializers.ListField(
        child=serializers.DictField()
    )

class ResultadoSerializer(serializers.ModelSerializer):
    test_nombre = serializers.CharField(source='test.nombre', read_only=True)
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Resultado
        fields = ['id', 'uuid', 'usuario_id', 'usuario_nombre', 'test_nombre', 'fecha',
                  'score_tiempo', 'score_metodos', 'score_entorno',
                  'area_debil_principal', 'recomendaciones']
        