from .models import Payment, Transaction
from django.db.models.signals import post_save
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import *
from django.contrib.contenttypes.models import ContentType

# ------------------------------------------ purchase payments signals ------------------------------------------
@receiver(post_save, sender=PurchaseItem)
@receiver(post_delete, sender=PurchaseItem)
def update_product_purchase_total(sender, instance, **kwargs):
    purchase = instance.purchase
    print(f"Signal triggered for purchase ID: {purchase.id}")
    purchase.calculate_total()
    print(f"New total: {purchase.total}")



@receiver(post_save, sender=Payment)
@receiver(post_delete, sender=Payment)
def update_purchase_amount(sender, instance, **kwargs):
    if instance.content_type and instance.content_type.model == 'purchase':
        purchase = Purchase.objects.get(id=instance.object_id)
        total_paid = Payment.objects.filter(
            content_type=instance.content_type,
            object_id=purchase.id
        ).aggregate(total_paid=models.Sum('amount'))['total_paid'] or 0
        purchase.amount = total_paid
        purchase.save()

# ------------------------------------------ inventory signals ------------------------------------------
@receiver(post_save, sender=Inventory)
def create_inventory_items(sender, instance, created, **kwargs):
    stock = ProductStock.objects.all()
    if created:
        for obj in stock:
            InventoryItem.objects.create(inventory=instance, product_stock=obj)

@receiver(post_save, sender=InventoryItem)
def handle_inventory_item_save(sender, instance, **kwargs):
    initiator = instance.inventory.initiator
    store = instance.inventory.store

    quantity_difference = instance.quantity_found - instance.quantity_expected

    if quantity_difference != 0:
        if quantity_difference > 0:
            type='input',
        if quantity_difference < 0:
            type='output',
        
        # Create StockOperation for excess inventory
        stock_operation, created = StockOperation.objects.get_or_create(
            initiator=initiator,
            store=store,
            type=type,
            subtype='difference',
            description=f"Difference d'inventaire {instance.inventory.id}"
        )
        StockOperationItem.objects.create(
            stock_operation=stock_operation,
            product_stock=instance.product_stock,
            quantity=abs(quantity_difference)
        )
        stock_operation.calculate_total()


# @receiver(post_save, sender=Inventory)
# def create_stock_difference(sender, instance, **kwargs):
#     initiator = instance.initiator
#     store = instance.store
#     items = instance.inventoryitem_set.all()

#     stock_input = None
#     stock_output = None

#     # Iterate through inventory items and calculate the difference
#     for item in items:
#         quantity_difference = item.quantity_found - item.quantity_expected

#         if quantity_difference > 0:
#             print('surplus')
#             # Create or update StockOperation for excess inventory
#             if not stock_input:
#                 stock_input = StockOperation.objects.create(
#                     initiator=initiator,
#                     store=store,
#                     type='difference',
#                     description=f'''Difference d'inventaire {instance.id}'''
#                 )
#             StockOperation.objects.create(
#                 stock_input=stock_input,
#                 product_stock=item.product_stock,
#                 quantity=quantity_difference
#             )
#         elif quantity_difference < 0:
#             print('defficit')
#             # Create or update StockOperation for deficit inventory
#             if not stock_output:
#                 stock_output = StockOperation.objects.create(
#                     initiator=initiator,
#                     store=store,
#                     type='difference',
#                     description=f"Difference d'inventaire {instance.id}"
#                 )
#             StockOperationItem.objects.create(
#                 stock_output=stock_output,
#                 product_stock=item.product_stock,
#                 quantity=abs(quantity_difference)
#             )

#     # Calculate totals for stock input and output
#     if stock_input:
#         stock_input.calculate_total()
#     if stock_output:
#         stock_output.calculate_total()



# ------------------------------------------ debts and receivables signals ------------------------------------------
@receiver(post_save, sender=Purchase)
def create_or_update_debt(sender, instance, **kwargs):

    content_type = ContentType.objects.get_for_model(sender)

    # Check if the purchase is partially paid
    if instance.amount < instance.total:
        Debt.objects.update_or_create(
            content_type=content_type,
            object_id=instance.id,
            defaults={
                'initiator': instance.initiator,
                'store': instance.store,
                'supplier': instance.supplier,
                'amount': instance.total - instance.amount,
                'label': instance.label,
                'description': instance.description,
                'due_date': instance.timestamp,  # Adjust if you have a different due date field
            }
        )
    else:
        # If the purchase is paid in full, set
        Debt.objects.filter(
            content_type=content_type,
            object_id=instance.id
        ).update(is_fully_paid=True)


@receiver(post_save, sender=Payment)
def create_or_update_receivable(sender, instance, **kwargs):
    if instance.content_type and instance.object_id:
        content_object = instance.content_object

        if isinstance(content_object, Sale):
            total_paid = sum(
                payment.amount for payment in Payment.objects.filter(
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
        else:
            print("Content object is not a Sale instance")
    else:
        print("Content type or object ID is None")


# ------------------------------------------ cashdesks and transactions signals------------------------------------------
@receiver(post_save, sender=Transaction)
def update_cashdesk_on_transaction_save(sender, instance, created, **kwargs):
    cashdesk = instance.payment.cashdesk
    if cashdesk:
        if instance.type == 'debit':
            cashdesk.debits += instance.amount
        elif instance.type == 'credit':
            cashdesk.credits += instance.amount

        # Update balance
        cashdesk.balance = abs(cashdesk.credits - cashdesk.debits)
        cashdesk.save()


@receiver(post_delete, sender=Transaction)
def update_cashdesk_on_transaction_delete(sender, instance, **kwargs):
    cashdesk = instance.payment.cashdesk
    if cashdesk:
        if instance.type == 'debit':
            cashdesk.debits -= instance.amount
        elif instance.type == 'credit':
            cashdesk.credits -= instance.amount

        # Update balance
        cashdesk.balance = abs(cashdesk.credits - cashdesk.debits)
        cashdesk.save()


@receiver(post_save, sender=ClosingCashReceipt)
def update_balance_found_on_save(sender, instance, **kwargs):
    instance.update_cashdesk_closing()


@receiver(post_delete, sender=ClosingCashReceipt)
def update_balance_found_on_delete(sender, instance, **kwargs):
    instance.update_cashdesk_closing()


@receiver(post_save, sender=Payment)
def create_or_update_transaction(sender, instance, created, **kwargs):
    if instance.content_type and instance.object_id:
        model_name = instance.content_type.model

        # Determine the transaction type
        if model_name == 'sale':
            transaction_type = 'credit'
        elif model_name in ['servicepurchase', 'purchase']:
            transaction_type = 'debit'
        else:
            print('No matching model found')
            return  # Skip creating or updating a transaction if it's not related to a sale or purchase

    else:
        transaction_type = 'credit'  # Default type if content_type or object_id is missing

    if created:
        # Create a new Transaction object
        Transaction.objects.create(
            payment=instance,
            type=transaction_type,
            amount=abs(instance.amount),  # Ensure amount is positive
            label=instance.label,
            audit='pending'
        )
        print(
            f'Transaction created: {transaction_type}, amount: {abs(instance.amount)}')
    else:
        # Update the existing Transaction object
        transaction = Transaction.objects.filter(payment=instance).first()
        if transaction:
            # Ensure amount is positive
            transaction.amount = abs(instance.amount)
            transaction.label = instance.label
            transaction.audit = 'pending'
            transaction.save()
            print(
                f'Transaction updated: {transaction_type}, amount: {abs(instance.amount)}')
        else:
            # Create a new Transaction object if none exists (optional safety net)
            Transaction.objects.create(
                payment=instance,
                type=transaction_type,
                amount=abs(instance.amount),  # Ensure amount is positive
                label=instance.label,
                audit='pending'
            )
            print(
                f'Transaction created: {transaction_type}, amount: {abs(instance.amount)}')


# ------------------------------------------ stocks operations signals------------------------------------------
@receiver(post_save, sender=StockOperationItem)
def update_product_stock_on_save(sender, instance, created, **kwargs):
    if created:
        product_stock = instance.product_stock
        stock_operation = instance.stock_operation
        if stock_operation.type == 'input':
            product_stock.quantity += instance.quantity
        elif stock_operation.type == 'output':
            product_stock.quantity -= instance.quantity
        product_stock.save()

    stock_operation.calculate_total()


@receiver(post_delete, sender=StockOperationItem)
def update_product_stock_on_delete(sender, instance, **kwargs):
    product_stock = instance.product_stock
    stock_operation = instance.stock_operation
    if stock_operation.type == 'input':
        product_stock.quantity -= instance.quantity
    elif stock_operation.type == 'output':
        product_stock.quantity += instance.quantity
    product_stock.save()

    stock_operation.calculate_total()
