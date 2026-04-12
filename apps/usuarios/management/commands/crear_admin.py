from django.core.management.base import BaseCommand
from apps.usuarios.models import Usuario

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        if not Usuario.objects.filter(username='admin').exists():
           u = Usuario.objects.create_superuser(
               username='admin',
               email='admin@ugmx.edu.mx',
               password='PassChange012',
               rol='admin'
           )
           self.stdout.write(self.style.SUCCESS(f'Administrador creado: {u.username}'))
        else:
            self.stdout.write(self.style.WARNING('El administrador ya existe.'))