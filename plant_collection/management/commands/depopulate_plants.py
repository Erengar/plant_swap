from plant_collection.models import Plant
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Depopulate plants'

    def handle(self, *args, **options):
        plants = Plant.objects.all()
        for plant in plants:
            if not plant.picture.all():
                plant.delete()
        self.stdout.write(self.style.SUCCESS('Plants cleaned!'))