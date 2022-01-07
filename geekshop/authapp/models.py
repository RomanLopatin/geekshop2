from datetime import timedelta, datetime
from django.conf import settings

import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users', blank=True)
    age = models.PositiveSmallIntegerField(default=18, verbose_name='Возраст')

    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_created = models.DateTimeField(blank=True, null=True)

    def is_activation_key_expired(self):
        if datetime.now() <= self.activation_key_created + timedelta(hours=48):
            return False
        return False
