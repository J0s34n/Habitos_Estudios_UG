from django.db import models
from django.utils import timezone

class Test(models.Model):
    AREAS = [
        ('tiempo', 'Organización y Gestión del Tiempo'),
        ('metodos', 'Métodos y Técnicas de Estudio'),
        ('entorno', 'Entorno y Actitudes Personales'),
    ]
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_modificacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='preguntas')
    texto = models.TextField()
    area = models.CharField(max_length=20, choices=Test.AREAS)
    orden = models.IntegerField(default=0)

    class Meta:
        ordering = ['orden']

class Opcion(models.Model):
    # Peso: 1=mejor hábito, 4=peor hábito
    PESOS = [(1,'Óptimo'),(2,'Regular'),(3,'Deficiente'),(4,'Crítico')]
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='opciones')
    texto = models.TextField()
    peso = models.IntegerField(choices=PESOS, default=1)
    letra = models.CharField(max_length=1)  # A, B, C, D