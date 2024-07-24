from django.db.models import Sum
import logging
from django.db import transaction
from .models import Transaction
from django.db.models.signals import post_save
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from .models import *
from django.contrib.contenttypes.models import ContentType

logger = logging.getLogger(__name__)

# ------------------------------------------ purchase transactions manager ------------------------------------------

@receiver(post_save, sender=PurchaseItem)
def increment_product_stock_on_purchaseitem_creation(sender, instance, created, **kwargs):
    if created:
        # Increment product stock on PurchaseItem creation
        product_stock = instance.product_stock
        product_stock.quantity += instance.quantity
        product_stock.save()
        purchase = instance.purchase
        purchase.calculate_total()


@receiver(pre_save, sender=PurchaseItem)
def adjust_product_stock_on_purchaseitem_update(sender, instance, **kwargs):
    if instance.pk:
        # Fetch the old quantity before update
        old_purchase_item = PurchaseItem.objects.get(pk=instance.pk)
        old_quantity = old_purchase_item.quantity

        # Adjust product stock based on the difference between old and new quantity
        product_stock = instance.product_stock
        new_quantity = instance.quantity
        quantity_difference = new_quantity - old_quantity
        product_stock.quantity += quantity_difference
        product_stock.save()
        purchase = instance.purchase
        purchase.calculate_total()


@receiver(pre_delete, sender=PurchaseItem)
def decrement_product_stock_on_purchaseitem_deletion(sender, instance, **kwargs):
    # Decrement product stock on PurchaseItem deletion
    product_stock = instance.product_stock
    product_stock.quantity -= instance.quantity
    if product_stock.quantity < 0:
        product_stock.quantity = 0  # Ensure quantity doesn't go below zero
    product_stock.save()
    purchase = instance.purchase
    purchase.calculate_total()


@receiver(pre_delete, sender=Purchase)
def update_product_stock_before_purchase_delete(sender, instance, **kwargs):

    if instance.type == 'product':
        # Fetch all items related to the purchase
        purchase_items = PurchaseItem.objects.filter(purchase=instance)

        for item in purchase_items:
            print(f'item quant : {item.quantity}')
            print(f'prod quant : {item.product_stock.quantity}')
            new_quantity = item.product_stock.quantity - item.quantity
            if new_quantity <= 0:
                new_quantity = 0
            item.product_stock.quantity = new_quantity
            item.product_stock.save()

            logger.info(
                f'Updated ProductStock {item.product_stock.id}: new quantity is {new_quantity}')
    else:
        pass


@receiver(post_save, sender=Transaction)
def update_purchase_total_paid(sender, instance, **kwargs):
    if instance.content_type and instance.content_type.model == 'purchase':
        purchase = Purchase.objects.get(id=instance.object_id)
        print(f'cashdesk : {instance.cashdesk}')
        total_paid = Transaction.objects.filter(
            content_type=instance.content_type,
            object_id=purchase.id
        ).aggregate(total_paid=models.Sum('amount'))['total_paid'] or 0
        purchase.total_paid = total_paid
        purchase.save()


@receiver(post_delete, sender=Purchase)
def delete_purchase_transactions(sender, instance, **kwargs):
    # Get the ContentType for the purchase model
    obj_content_type = ContentType.objects.get_for_model(Purchase)

    # Delete all transactions related to this purchase
    transactions = Transaction.objects.filter(
        content_type=obj_content_type, object_id=instance.id
    )

    for transaction in transactions:
        logger.info(f'Updating cashdesk for transaction: {transaction.id}')
        transaction.cashdesk.debits -= transaction.amount
        transaction.cashdesk.save()

    transactions.delete()


# ------------------------------------------ inventory manager ------------------------------------------
@receiver(post_save, sender=Inventory)
def create_inventory_items(sender, instance, created, **kwargs):
    stock = ProductStock.objects.all()
    if created:
        for obj in stock:
            InventoryItem.objects.create(inventory=instance, product_stock=obj)


# ------------------------------------------ debts and receivables signals ------------------------------------------
@receiver(post_save, sender=Transaction)
def create_or_update_receivable_or_debt(sender, instance, **kwargs):

    if instance.content_type and instance.object_id:
        content_object = instance.content_object

        if isinstance(content_object, Sale):
            total_paid = sum(
                transaction.amount for transaction in Transaction.objects.filter(
                    content_type=instance.content_type,
                    object_id=instance.object_id
                )
            )
            content_object.total_paid = total_paid
            content_object.save()

            if content_object.total_paid < content_object.total:
                Receivable.objects.update_or_create(
                    sale=content_object,
                    client=content_object.client,
                    defaults={'amount': content_object.total_due,
                              'due_date': timezone.now() + timezone.timedelta(days=30)}
                )
            else:
                Receivable.objects.filter(
                    sale=content_object).update(is_fully_paid=True)

        elif isinstance(content_object, Purchase):
            total_paid = sum(
                transaction.amount for transaction in Transaction.objects.filter(
                    content_type=instance.content_type,
                    object_id=instance.object_id
                )
            )
            content_object.total_paid = total_paid
            content_object.save()

            if content_object.total_paid < content_object.total:
                Debt.objects.update_or_create(
                    purchase=content_object,
                    supplier=content_object.supplier,
                    defaults={'amount': content_object.total_due,
                              'due_date': timezone.now() + timezone.timedelta(days=30)}
                )
            else:
                Debt.objects.filter(
                    purchase=content_object).update(is_fully_paid=True)

        else:
            print("Content object is neither a Sale nor a Purchase instance")
    else:
        print("Content type or object ID is None")


# cashdesks signals------------------------------------------
@receiver(pre_save, sender=Transaction)
def track_previous_transaction_amount(sender, instance, **kwargs):
    if instance.pk:
        previous_transaction = Transaction.objects.get(pk=instance.pk)
        instance._previous_amount = previous_transaction.amount
        instance._previous_type = previous_transaction.type
    else:
        instance._previous_amount = None
        instance._previous_type = None


@receiver(post_save, sender=Transaction)
def update_cashdesk_on_transaction_save(sender, instance, created, **kwargs):
    cashdesk = instance.cashdesk
    if cashdesk:
        if not created and instance._previous_amount is not None:
            if instance._previous_type == 'debit':
                cashdesk.debits -= instance._previous_amount
            elif instance._previous_type == 'credit':
                cashdesk.credits -= instance._previous_amount

        if instance.type == 'debit':
            cashdesk.debits += instance.amount
        elif instance.type == 'credit':
            cashdesk.credits += instance.amount

        # Update balance
        cashdesk.balance = abs(cashdesk.credits - cashdesk.debits)
        cashdesk.save()

        # Recalculate to ensure consistency
        recalculate_cashdesk_balances(cashdesk)


@receiver(post_delete, sender=Transaction)
def update_cashdesk_on_transaction_delete(sender, instance, **kwargs):
    cashdesk = instance.cashdesk
    if cashdesk:
        if instance.type == 'debit':
            cashdesk.debits -= instance.amount
        elif instance.type == 'credit':
            cashdesk.credits -= instance.amount

        # Update balance
        cashdesk.balance = abs(cashdesk.credits - cashdesk.debits)
        cashdesk.save()

        # Recalculate to ensure consistency
        recalculate_cashdesk_balances(cashdesk)


def recalculate_cashdesk_balances(cashdesk):
    credits = Transaction.objects.filter(cashdesk=cashdesk, type='credit').aggregate(
        total=models.Sum('amount'))['total'] or 0
    debits = Transaction.objects.filter(cashdesk=cashdesk, type='debit').aggregate(
        total=models.Sum('amount'))['total'] or 0
    cashdesk.credits = credits
    cashdesk.debits = debits
    cashdesk.balance = credits - debits
    cashdesk.save()

# cashdesks closing signals------------------------------------------


@receiver(post_save, sender=ClosingCashReceipt)
def update_balance_found_on_save(sender, instance, **kwargs):
    instance.update_cashdesk_closing()


@receiver(post_delete, sender=ClosingCashReceipt)
def update_balance_found_on_delete(sender, instance, **kwargs):
    instance.update_cashdesk_closing()


# ------------------------------------------ stocks operations signals------------------------------------------
# @receiver(post_save, sender=StockOperationItem)
# def update_product_stock_on_save(sender, instance, created, **kwargs):
#     product_stock = instance.product_stock
#     stock_operation = instance.stock_operation

#     if created:
#         if stock_operation.type == 'input':
#             product_stock.quantity += instance.quantity
#         elif stock_operation.type == 'output':
#             product_stock.quantity -= instance.quantity
#         product_stock.save()

#     # Update stock operation total after product stock has been updated
#     stock_operation.calculate_total()
#     stock_operation.save()


# @receiver(post_delete, sender=StockOperationItem)
# def update_product_stock_on_delete(sender, instance, **kwargs):
#     product_stock = instance.product_stock
#     stock_operation = instance.stock_operation
#     if stock_operation.type == 'input':
#         product_stock.quantity -= instance.quantity
#     elif stock_operation.type == 'output':
#         product_stock.quantity += instance.quantity
#     product_stock.save()

#     stock_operation.calculate_total()


# ------------------------------------------ product stock update from purchase ------------------------------------------
@receiver(post_save, sender=Purchase)
def create_or_update_stockops_from_purchase(sender, instance, created, **kwargs):
    if instance.type == 'product':
        # Check if a StockOperation already exists for this Purchase
        stock_operation, created_op = StockOperation.objects.update_or_create(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id,
            defaults={
                'type': 'input',
                'subtype': 'purchase',
                'store': instance.store,
                'initiator': instance.initiator,
                'content_object': instance
            }
        )

        # Optionally handle items if necessary
        stock_operation.items = instance.purchaseitem_set.count()
        stock_operation.total = sum(
            item.quantity for item in instance.purchaseitem_set.all())
        stock_operation.save()


@receiver(post_save, sender=Purchase)
def update_product_stock_after_purchase(sender, created, instance, **kwargs):
    # Fetch all SaleItems related to the Sale
    items = PurchaseItem.objects.filter(purchase=instance)

    for item in items:
        # Update the quantity of the related ProductStock
        item.product_stock.quantity += item.quantity
        item.product_stock.save()


@receiver(post_save, sender=PurchaseItem)
def update_stock_operation_item_from_purchase_item(sender, instance, created, **kwargs):
    product_stock = instance.product_stock
    purchase = instance.purchase
    product_stock.quantity = instance.quantity
    print(f'new stock quantity : {instance.quantity}')
    product_stock.save()
    # Ensure the StockOperation is created or updated
    stock_operation, created_op = StockOperation.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(purchase),
        object_id=purchase.id,
        defaults={
            'type': 'input',
            'subtype': 'purchase',
            'store': purchase.store,
            'initiator': purchase.initiator
        }
    )

    # Create or update the StockOperationItem
    StockOperationItem.objects.update_or_create(
        stock_operation=stock_operation,
        product_stock=product_stock,
        defaults={'quantity': instance.quantity}
    )


@receiver(post_delete, sender=PurchaseItem)
def update_prodstock_from_purchase_item_delete(sender, instance, **kwargs):
    product_stock = instance.product_stock
    purchase = instance.purchase

    # Subtract the quantity of the deleted purchase item from the product stock
    product_stock.quantity -= instance.quantity
    product_stock.save()

    # Ensure the StockOperation is updated
    try:
        stock_operation = StockOperation.objects.get(
            content_type=ContentType.objects.get_for_model(purchase),
            object_id=purchase.id,
            type='input',
            subtype='purchase'
        )

        # Update or delete the StockOperationItem
        stock_op_item = StockOperationItem.objects.get(
            stock_operation=stock_operation,
            product_stock=product_stock
        )

        stock_op_item.quantity -= instance.quantity
        if stock_op_item.quantity <= 0:
            stock_op_item.delete()
        else:
            stock_op_item.save()

        # Recalculate the total items in the StockOperation
        stock_operation.total = sum(
            item.quantity for item in stock_operation.stockoperationitem_set.all()
        )
        stock_operation.save()
    except StockOperation.DoesNotExist:
        pass  # Handle the case where the stock operation does not exist
    except StockOperationItem.DoesNotExist:
        pass  # Handle the case where the stock operation item does not exist



# ------------------------------------------ Sale signals ------------------------------------------
# product stock update from sale ------------------------
@receiver(post_save, sender=Sale)
def create_or_update_stockops_from_sale(sender, instance, **kwargs):
    stock_operation, created = StockOperation.objects.update_or_create(
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id,
        defaults={
            'store': instance.store,
            'initiator': instance.initiator,
            'type': 'output',  # or other appropriate value
            'subtype': 'sale',  # or other appropriate value
            'description': 'Sale operation',
            'total': instance.total,  # or other appropriate value
        }
    )
    # Other logic as needed


@receiver(post_save, sender=SaleItem)
# @receiver(post_delete, sender=SaleItem)
def update_prodstock_from_sale_item(sender, instance, created, **kwargs):
    sale = instance.sale
    print(f"Signal triggered for sale ID: {sale.id}")
    sale.calculate_total()
    print(f"New total: {sale.total}")
    product_stock = instance.product_stock

    if created:
        # Remove the quantity of the new sale item from the product stock
        product_stock.quantity -= instance.quantity
    else:
        try:
            previous_instance = SaleItem.objects.get(pk=instance.pk)
            quantity_difference = instance.quantity + previous_instance.quantity
            product_stock.quantity -= quantity_difference
        except SaleItem.DoesNotExist:
            product_stock.quantity -= instance.quantity

    product_stock.save()

    # Ensure the StockOperation is created or updated
    sale = instance.sale
    stock_operation, created = StockOperation.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(sale),
        object_id=sale.id,
        type='output',
        subtype='sale',
        store=sale.store,
        initiator=sale.initiator
    )

    # Create or update the StockOperationItem
    StockOperationItem.objects.update_or_create(
        stock_operation=stock_operation,
        product_stock=product_stock,
        defaults={'quantity': instance.quantity}
    )


@receiver(post_delete, sender=Sale)
def delete_sale_transactions(sender, instance, **kwargs):
    obj_content_type = ContentType.objects.get_for_model(Sale)

    # Handle transactions
    transactions = Transaction.objects.filter(
        content_type=obj_content_type, object_id=instance.id
    )
    for transaction in transactions:
        logger.info(f'Updating cashdesk for transaction: {transaction.id}')
        transaction.cashdesk.credits -= transaction.amount
        transaction.cashdesk.save()
    transactions.delete()


@receiver(pre_delete, sender=Sale)
def update_product_stock_before_sale_delete(sender, instance, **kwargs):
    # Fetch all SaleItems related to the Sale
    sale_items = SaleItem.objects.filter(sale=instance)

    for item in sale_items:
        # Update the quantity of the related ProductStock
        item.product_stock.quantity += item.quantity
        item.product_stock.save()


# sale total_paid update from transaction ------------------------
@receiver(post_delete, sender=Transaction)
def update_sale_total_paid_on_transaction_delete(sender, instance, **kwargs):
    # Get the Sale object related to this transaction
    try:
        sale_content_type = ContentType.objects.get_for_model(Sale)
        if instance.content_type == sale_content_type:
            sale = Sale.objects.get(id=instance.object_id)
            if sale:
                sale.total_paid -= instance.amount
                sale.save()
    except Sale.DoesNotExist:
        pass  # Handle the case where the Sale object does not exist


@receiver(post_save, sender=ProductStock)
def correct_product_stock(sender, instance, **kwargs):
    ins = PurchaseItem.objects.filter(product_stock=instance)
    outs = SaleItem.objects.filter(product_stock=instance)

    ins_aggregate = ins.aggregate(totals=Sum('quantity'))['totals'] or 0
    outs_aggregate = outs.aggregate(totals=Sum('quantity'))['totals'] or 0

    final_quantity = ins_aggregate - outs_aggregate

    instance.quantity = final_quantity

