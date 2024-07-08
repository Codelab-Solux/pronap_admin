
from django import template
from django.shortcuts import get_object_or_404
from base.models import *
from django.db.models import Sum

register = template.Library()

@register.filter
def get_input_count(pk):
    product = ProductStock.objects.get(id=pk)
    input_items = StockInputItem.objects.filter(product_stock = product)
    # item_count = input_items.aggregate(total_quantity=Sum('quantity'))[
    #     'total_quantity'] or 0

    item_count = 0
    for obj in input_items:
        item_count = obj.quantity + item_count

    return item_count


@register.filter
def get_output_count(pk):
    product = ProductStock.objects.get(id=pk)
    input_items = StockOutputItem.objects.filter(product_stock = product)
    item_count = input_items.aggregate(total_quantity=Sum('quantity'))[
        'total_quantity'] or 0

    return item_count


@register.filter
def get_final_stock(pk):
    input = get_input_count(pk)
    output = get_output_count(pk)
    item_count = input - output

    return item_count


@register.filter
def get_stock_value(pk):
    product = ProductStock.objects.get(id=pk)
    stock = get_final_stock(pk)
    value = stock * product.price

    return value

@register.filter
def get_purchases_count(pk):
    client = Client.objects.get(id=pk)
    sales_count = Sale.objects.filter(client = client).count()

    return sales_count

@register.filter
def get_purchases_value(pk):
    client = Client.objects.get(id=pk)
    sales = Sale.objects.filter(client = client)
    sales_value = sales.aggregate(totals=Sum('total'))['totals'] or 0

    return sales_value
