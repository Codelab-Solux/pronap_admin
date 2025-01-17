
from django import template
from django.shortcuts import get_object_or_404
from base.models import *
from django.db.models import Sum

register = template.Library()


@register.filter
def get_input_count(pk):
    product = ProductStock.objects.get(id=pk)
    items = StockOperationItem.objects.filter(
        product_stock=product, stock_operation__type='input')

    item_count = 0
    for obj in items:
        item_count = obj.quantity + item_count

    return item_count


@register.filter
def get_output_count(pk):
    product = ProductStock.objects.get(id=pk)
    items = StockOperationItem.objects.filter(product_stock=product, stock_operation__type='output')
    item_count = items.aggregate(total_quantity=Sum('quantity'))[
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
    sales_count = Sale.objects.filter(client=client).count()

    return sales_count


@register.filter
def get_purchases_value(pk):
    client = Client.objects.get(id=pk)
    sales = Sale.objects.filter(client=client)
    sales_value = sales.aggregate(totals=Sum('total'))['totals'] or 0

    return sales_value


@register.filter
def get_desk_receipt(pk, kp):
    closing = CashdeskClosing.objects.filter(id=pk).first()
    cash_receipt = CashReceipt.objects.filter(id=kp).first()
    result = ClosingCashReceipt.objects.filter(
        cash_receipt=cash_receipt, CashdeskClosing=closing).first()
    return result


@register.filter
def get_debt_payments(pk):
    content_type = ContentType.objects.get_for_model(Purchase)
    debt = Debt.objects.filter(id=pk).first()
    pay_transactions = Transaction.objects.filter(content_type=content_type, object_id=debt.purchase.id)
    pay_aggregate = pay_transactions.aggregate(
        amount=models.Sum('amount'))['amount'] or 0
    return pay_aggregate

@register.filter
def get_receivable_payments(pk):
    content_type = ContentType.objects.get_for_model(Sale)
    receivable = Receivable.objects.filter(id=pk).first()
    pay_transactions = Transaction.objects.filter(content_type=content_type, object_id=receivable.purchase.id)
    pay_aggregate = pay_transactions.aggregate(
        amount=models.Sum('amount'))['amount'] or 0
    return pay_aggregate




# in template arithmetic----------------------------------------

@register.filter
def add(a, b):
    try:
        return int(a) + int(b)
    except (ValueError, TypeError):
        return ''

@register.filter
def subtract(a, b):
    try:
        return int(a) - int(b)
    except (ValueError, TypeError):
        return ''

@register.filter
def multiply(a, b):
    try:
        return int(a) * int(b)
    except (ValueError, TypeError):
        return ''
    
@register.filter
def divide(a, b):
    try:
        return int(a) / int(b)
    except (ValueError, TypeError):
        return ''
