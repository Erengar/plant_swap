import csv
from plant_collection.models import Species
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Populate species from csv file'

    def handle(self, *args, **options):
        Species.objects.all().delete()
        with open('static/species.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for line in csv_reader:
                Species.objects.get_or_create(name=line[0])
        self.stdout.write(self.style.SUCCESS('Species added to database!'))