import json
import os
from django.core.management.base import BaseCommand
from lead.models import Industry, Product
from django.conf import settings

class Command(BaseCommand):
    help = 'Load products for an industry from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('industry_name', type=str, help='Name of the industry')
        parser.add_argument('json_file', type=str, help='Path to the JSON file containing products')

    def handle(self, *args, **kwargs):
        industry_name = kwargs['industry_name']
        json_file = kwargs['json_file']
        fixture_path = os.path.join(settings.BASE_DIR, 'lead', 'fixtures', json_file)

        if not os.path.exists(fixture_path):
            self.stdout.write(self.style.ERROR(f"JSON file '{json_file}' does not exist"))
            return

        try:
            industry = Industry.objects.get(name=industry_name)
        except Industry.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Industry '{industry_name}' does not exist"))
            return

        with open(fixture_path, 'r') as file:
            data = json.load(file)

        for product_data in data:
            name = product_data.get('name')
            description = product_data.get('description')
            granual_type = product_data.get('granual_type')
            
            if name:
                product, created = Product.objects.get_or_create(industry=industry, name=name, granual_type=granual_type, description=description)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Product '{name}' created"))
                else:
                    self.stdout.write(self.style.WARNING(f"Product '{name}' already exists"))
            else:
                self.stdout.write(self.style.ERROR("Name is required for each product"))

        self.stdout.write(self.style.SUCCESS('Products loaded successfully'))
