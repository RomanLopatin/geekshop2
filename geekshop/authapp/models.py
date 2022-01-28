from datetime import timedelta, datetime
from django.conf import settings

import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

NULLABLE = {'blank': True, 'null': True}


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users', blank=True)
    age = models.PositiveSmallIntegerField(default=18, verbose_name='Возраст')

    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_created = models.DateTimeField(blank=True, null=True)

    def is_activation_key_expired(self):
        if datetime.now() <= self.activation_key_created + timedelta(hours=48):
            return False
        return False


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    UNNOWN = 'u'

    GENDERS = (
        (MALE, 'М'),
        (FEMALE, 'Ж'),
        (UNNOWN, 'Н'),
    )

    user = models.OneToOneField(ShopUser, unique=True, null=False,
                                db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=128, **NULLABLE)
    aboutMe = models.TextField(verbose_name='о себе', max_length=512, **NULLABLE)
    gender = models.CharField(verbose_name='пол', max_length=1,
                              choices=GENDERS, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
