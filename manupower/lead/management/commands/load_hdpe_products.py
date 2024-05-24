import json
import os
from django.core.management.base import BaseCommand
from lead.models import Category, Product
from django.conf import settings

class Command(BaseCommand):
    help = 'Load initial data into Category and Product models from a JSON file'

    def handle(self, *args, **kwargs):
        fixture_path = os.path.join(settings.BASE_DIR, 'lead', 'fixtures', 'hdpe_products.json')
        with open(fixture_path, 'r') as file:
            data = json.load(file)

        for item in data['HDPE_Products']:
            category_name = item['category']
            product_name = item['product']
            
            # Ensure category exists
            category, created = Category.objects.get_or_create(name=category_name, defaults={'granual_type': 'HDPE'})
            
            # Create product
            Product.objects.create(name=product_name, category=category)

        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data'))
