import json

from django.conf import settings
from django.core.management import BaseCommand

from authapp.models import ShopUser, ShopUserProfile
from mainapp.models import ProductCategotry, Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in ShopUser.objects.all():
            # if not user.shopuserprofile:
            ShopUserProfile.objects.create(user=user)
            # users_profile = ShopUserProfile.objects.create(user=user)
            # users_profile.save()
