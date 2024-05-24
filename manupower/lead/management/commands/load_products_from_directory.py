import json
import os
from glob import glob
from django.core.management.base import BaseCommand
from lead.models import Industry, Product
from django.conf import settings

class Command(BaseCommand):
    help = 'Load products for industries from all JSON files in the specified directory'

    def handle(self, *args, **kwargs):
        fixture_directory = os.path.join(settings.BASE_DIR, 'lead', 'fixtures', 'products')

        if not os.path.isdir(fixture_directory):
            self.stdout.write(self.style.ERROR(f"Directory '{fixture_directory}' does not exist"))
            return

        json_files = glob(os.path.join(fixture_directory, '*.json'))

        if not json_files:
            self.stdout.write(self.style.ERROR(f"No JSON files found in directory '{fixture_directory}'"))
            return

        for json_file in json_files:
            with open(json_file, 'r') as file:
                data = json.load(file)

            for product_data in data:
                industry_name = product_data.get('industry')
                name = product_data.get('name')
                description = product_data.get('description')
                granual_type = product_data.get('granual_type')

                if not industry_name or not name:
                    self.stdout.write(self.style.ERROR(f"Missing 'industry' or 'name' in file '{json_file}'"))
                    continue

                industry, created = Industry.objects.get_or_create(name=industry_name)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Industry '{industry_name}' created"))

                product, created = Product.objects.get_or_create(
                    industry=industry,
                    name=name,
                    defaults={'description': description, 'granual_type': granual_type}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Product '{name}' created in industry '{industry_name}'"))
                else:
                    self.stdout.write(self.style.WARNING(f"Product '{name}' already exists in industry '{industry_name}'"))

        self.stdout.write(self.style.SUCCESS('Products loaded successfully'))
