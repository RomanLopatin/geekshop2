from django.db import transaction
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from django.shortcuts import render, get_object_or_404

# Create your views here.
from basketapp.models import Basket
# from ordersapp.forms import OrderItemForm
from mainapp.models import Product
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderListView(ListView):
    # здесь шаблон можно не оказывать, поскольку для данного имени класса и структуры папок шаблонов
    # автоматом будет вестись поиск шаблона в папке  /templates/order_list.html
    model = Order

    def get_queryset(self):
        # return super().get_queryset().filter(is_active=True)
        return super().get_queryset().filter(is_active=True).select_related()


class OrderCreateView(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            # basket_items = Basket.objects.filter(user=self.request.user)
            basket_items = Basket.objects.filter(user=self.request.user).select_related()
            if len(basket_items):
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=len(basket_items))
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
            else:
                formset = OrderFormSet()

        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()
            # basket_items = Basket.objects.filter(user=self.request.user)
            basket_items = Basket.objects.filter(user=self.request.user).select_related()
            basket_items.delete()

        # удаляем пустой заказ
        if self.object.get_summary()['total_cost'] == 0:
            self.object.delete()
        #
        return super().form_valid(form)


class OrderUpdateView(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('ordersapp:list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            # formset = OrderFormSet(instance=self.object)
            queryset = self.object.orderitems.select_related()
            formset = OrderFormSet(instance=self.object, queryset=queryset)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        context_data['orderitems'] = formset
        return context_data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        if self.object.get_summary()['total_cost'] == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('ordersapp:list')


class OrderDetailView(DetailView):
    model = Order


def order_complete_view(request, pk):
    order_item = Order.objects.get(pk=pk)
    order_item.status = Order.STATUS_SENT_TO_PROCEED
    order_item.save()

    return HttpResponseRedirect(reverse('ordersapp:list'))


@receiver(pre_save, sender=OrderItem)
# @receiver(pre_save, sender=Basket)
def product_quantity_update_on_save(sender, update_fields, instance, **kwargs):
    if instance.pk:
        instance.product.quantity -= instance.quantity - sender.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
# @receiver(pre_delete, sender=Basket)
def product_quantity_update_on_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()


def get_product_price(request, pk):
    _price = 0
    # if request.is_ajax():
    #     _product = get_object_or_404(Product, pk=pk)
    _product = Product.objects.get(pk=int(pk))
    if _product:
        _price = _product.price

    return JsonResponse({'price': _price})
