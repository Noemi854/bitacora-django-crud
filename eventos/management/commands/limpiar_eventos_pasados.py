from django.core.management.base import BaseCommand
from eventos.models import eventos
from datetime import date

class Command(BaseCommand):
    help = 'Elimina eventos cuya fecha ya pasó'

    def handle(self, *args, **options):
        hoy = date.today()
        eventos_eliminados = eventos.objects.filter(fecha_evento__lt=hoy).delete()
        
        cantidad = eventos_eliminados[0]
        self.stdout.write(
            self.style.SUCCESS(f'Se eliminaron {cantidad} eventos pasados correctamente')
        )
