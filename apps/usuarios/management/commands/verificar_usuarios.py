from django.core.management.base import BaseCommand
from apps.usuarios.models import Usuario

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for u in Usuario.objects.all():
            self.stdout.write(
                f"{u.username} | rol: {u.rol} | is_staff: {u.is_staff} | is_superuser: {u.is_superuser}"
            )