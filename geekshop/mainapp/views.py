import json
import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
from mainapp import models
from mainapp.models import Product, ProductCategotry


def get_hot_product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]


def get_same_products(hot_product):
    same_products_list = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)
    return same_products_list[:3]


def index(request):
    product_list = Product.objects.all()[:4]
    context = {
        'title': 'магазин',
        'products': product_list,
    }
    return render(request, "mainapp/index.html", context)


def products(request, pk=None, page=1):
    links_menu = ProductCategotry.objects.filter(is_active=True)
    title = 'продукты'

    if pk is not None:
        if pk == 0:
            product_list = Product.objects.filter(is_active=True, category__is_active=True)
            category_item = {'name': 'все', 'pk': 0}
        else:
            category_item = get_object_or_404(ProductCategotry, pk=pk)
            product_list = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True)

        paginator = Paginator(product_list, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'products': products_paginator,
            'category': category_item,
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()

    content = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product),
    }

    return render(request, 'mainapp/products.html', content)


def contact(request):
    with open("json/contact_info.json") as read_f:
        adresses = json.load(read_f)

    context = {
        'title': 'Контакты',
        'addresses': adresses,
    }
    return render(request, "mainapp/contact.html", context)


def context(request):
    with open("json/my.json") as read_f:
        some_info = json.load(read_f)

    context = {
        'title': "Title",
        'header': "header",
        'username': "Джон",
        'products': [{'name': 'one', 'price': 1}, {'name': 'two', 'price': 10}, {'name': 'three', 'price': 15}]
    }
    return render(request, "mainapp/test_context.html", context)


def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': ProductCategotry.objects.filter(is_active=True),
        'product': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'mainapp/product.html', content)
