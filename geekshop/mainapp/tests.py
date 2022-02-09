from django.test import TestCase
from django.test.client import Client
from mainapp.models import Product, ProductCategotry
from django.core.management import call_command


# Create your tests here.
class TestMainappSmoke(TestCase):
    status_code_success = 200

    def setUp(self) -> None:
        # call_command('flush', '--noinput')
        # call_command('loaddata', 'data.json')
        category = ProductCategotry.objects.create(
            name='cat1'
        )
        for i in range(1, 10):
            Product.objects.create(
                category=category,
                name=f'prod#{i}'
            )
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, self.status_code_success)

        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, self.status_code_success)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, self.status_code_success)

    def test_categories_urls(self):
        response = self.client.get('/products/0')
        self.assertEqual(response.status_code, self.status_code_success)

        for cat in ProductCategotry.objects.all():
            response = self.client.get(f'/products/{cat.pk}')
            self.assertEqual(response.status_code, self.status_code_success)

    def test_product_urls(self):
        for prod in Product.objects.all():
            response = self.client.get(f'/products/product/{prod.pk}/')
            self.assertEqual(response.status_code, self.status_code_success)


