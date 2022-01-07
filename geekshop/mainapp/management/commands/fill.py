import json

from django.conf import settings
from django.core.management import BaseCommand

from authapp.models import ShopUser
from mainapp.models import ProductCategotry, Product


def load_from_json(file_name):
    with open(f"{settings.BASE_DIR}/json/{file_name}.json", encoding='utf-8') as json_file:
        return json.load(json_file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')
        ProductCategotry.objects.all().delete()
        for cat in categories:
            ProductCategotry.objects.create(**cat)
        # print(categories)
        #

        products = load_from_json('products')
        print(products)
        Product.objects.all().delete()

        for product in products:
            category_name = product['category']
            _category = ProductCategotry.objects.get(name=category_name)
            product['category'] = _category
            Product.objects.create(**product)

        super_user = ShopUser.objects.create_superuser(
            'django',
            'django@geekshop.local',
            'geekbrains',
            age=33

        )
