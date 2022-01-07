from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='media_for_users')
def media_for_users(avatar):
    if not avatar:
        avatar = 'users/product-5-sm.jpg'

    return f'{settings.MEDIA_URL}{avatar}'


# @register.filter(name='media_for_products')
def media_for_products(product):
    if not product:
        product = 'products_images/product-1.jpg'

    return f'{settings.MEDIA_URL}{product}'


register.filter('media_for_products', media_for_products)  # второй способ регистрации фильтра
# register.filter('media_folder_products', media_folder_products)
