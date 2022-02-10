from django.core.management.base import BaseCommand

from adminapp.views import db_profile_by_type
from mainapp.models import ProductCategotry, Product
from django.db import connection
from django.db.models import Q


class Command(BaseCommand):
    def handle(self, *args, **options):
        test_products = Product.objects.filter(
            Q(category__name='офис') |
            Q(category__name='модерн')
        ).select_related()
        db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
        print(test_products)
        db_profile_by_type('learn', '', connection.queries)

