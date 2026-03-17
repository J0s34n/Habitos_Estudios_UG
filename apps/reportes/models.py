from django.db import models
from django.conf import settings

class Reporte(models.Model):
    TIPOS = [
        ('general', 'Análisis General de Hábitos'),
        ('comparativa', 'Comparativa por Test'),
        ('criticas', 'Áreas Críticas de Atención'),
    ]

    tipo = models.CharField(max_length=20, choices=TIPOS)
    generado_por = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    # Datos del reporte guardados como JSON
    datos = models.JSONField(default=dict)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.fecha:%d/%m/%Y}"