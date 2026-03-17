from rest_framework import serializers
from .models import Reporte

class ReporteSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    generado_por_nombre = serializers.CharField(
        source='generado_por.username', read_only=True
    )

    class Meta:
        model = Reporte
        fields = ['id', 'tipo', 'tipo_display', 'generado_por_nombre', 'fecha', 'datos']
        read_only_fields = ['id', 'fecha', 'generado_por_nombre', 'datos']