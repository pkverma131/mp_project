import json
import os
from django.core.management.base import BaseCommand
from lead.models import Industry
from django.conf import settings

class Command(BaseCommand):
    help = 'Load industries from a JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file containing industries')

    def handle(self, *args, **kwargs):
        json_file = kwargs['json_file']
        fixture_path = os.path.join(settings.BASE_DIR, 'lead', 'fixtures', json_file)

        if not os.path.exists(fixture_path):
            self.stdout.write(self.style.ERROR(f"JSON file '{json_file}' does not exist"))
            return

        with open(fixture_path, 'r') as file:
            data = json.load(file)

        for industry_data in data['categories']:
            name = industry_data.get('name')
            description = industry_data.get('description')
            
            if name:
                industry, created = Industry.objects.get_or_create(name=name, defaults={'description': description})
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Industry '{name}' created"))
                else:
                    self.stdout.write(self.style.WARNING(f"Industry '{name}' already exists"))
            else:
                self.stdout.write(self.style.ERROR("Name and granual_type are required for each industry"))

        self.stdout.write(self.style.SUCCESS('Industries loaded successfully'))
