import csv
from plant_collection.models import Plant, Species
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import random


class Command(BaseCommand):
    help = 'Populate plants from csv file'

    def handle(self, *args, **options):
        with open('static/plants.csv', 'r', encoding='utf8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for line in csv_reader:
                for_trade = False
                if random.randint(0, 10) > 5:
                    for_trade = True
                Plant.objects.get_or_create(nick_name=line[0],
                                        owner=User.objects.get(username='Polo'),
                                        for_trade=for_trade,
                                        location=line[1],
                                        species=Species.objects.get(name='Snake Plant'),
                                        )
        self.stdout.write(self.style.SUCCESS('Plants added to database!'))