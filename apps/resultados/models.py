from django.db import models
from django.conf import settings
from apps.tests_app.models import Test, Pregunta, Opcion
import uuid

class Resultado(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resultados')
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    # Puntajes por area (0-100, mayor es debil)
    # Podemos calcular esto al guardar el resultado, o hacerlo dinámicamente al mostrarlo 
    score_tiempo = models.FloatField(default=0)  # Puntaje para el área de tiempo 
    score_metodos = models.FloatField(default=0)  # Puntaje para el área de métodos de estudio 
    score_entorno = models.FloatField(default=0)  # Puntaje para el área de entorno de estudio
    area_debil_principal = models.CharField(max_length=20)  # Área más débil identificada
    # Recomendaciones personalizadas basadas en el área débil principal
    recomendaciones = models.JSONField(default=list)  # Almacena recomendaciones específicas para el usuario

    class Meta:
        ordering = ['-fecha']

class RespuestaDetalle(models.Model):
    resultado = models.ForeignKey(Resultado, on_delete=models.CASCADE, related_name='respuestas')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    opcion_seleccionada = models.ForeignKey(Opcion, on_delete=models.CASCADE)
    
