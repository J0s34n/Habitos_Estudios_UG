from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Usuario(AbstractUser):
    ROLES = [ ('admin', 'Administrador'), ('estudiante', 'Estudiante'), ('profesor', 'Profesor') ]
    primer_apellido = models.CharField(max_length=100, blank=True)
    segundo_apellido = models.CharField(max_length=100, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')
    matricula = models.CharField(max_length=20, blank=True, unique=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Superusuario y Staff deben ser administradores
    @property
    def es_admin(self):
        return self.rol == 'admin' or self.is_superuser or self.is_staff

    def __str__(self):
        return f"{self.get_full_name()} - ({self.rol})"
    
class Queja(models.Model):
    TIPOS = [('queja', 'Queja'), ('sugerencia', 'Sugerencia')]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tipo = models.CharField(max_length=50, choices=TIPOS)
    comentario = models.TextField()
    email = models.EmailField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tipo()} - {self.email} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
              