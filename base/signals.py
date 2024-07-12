from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import *
from django.contrib.contenttypes.models import ContentType

# transaction manager
@receiver(post_save, sender=Sale)
def create_sale_transaction(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            initiator=instance.initiator,
            store=instance.store,
            cashdesk=instance.cashdesk,
            type='credit',
            label='Vente de produit(s)',
            amount=instance.total,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )
    else:
        Transaction.objects.filter(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        ).update(
            amount=instance.total,
            cashdesk=instance.cashdesk,
            store=instance.store,
            initiator=instance.initiator,
        )

@receiver(post_save, sender=SaleItem)
@receiver(post_delete, sender=SaleItem)
def update_sale_total(sender, instance, **kwargs):
    instance.sale.calculate_total()

@receiver(post_save, sender=ProductPurchase)
def create_product_purchase_transaction(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            initiator=instance.store,
            store=instance.store,
            cashdesk=instance.cashdesk,
            type='debit',
            amount=instance.total,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )
    else:
        Transaction.objects.filter(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        ).update(
            amount=instance.total,
            cashdesk=instance.cashdesk,
            store=instance.store,
            initiator=instance.store,
        )

@receiver(post_save, sender=PurchaseItem)
@receiver(post_delete, sender=PurchaseItem)
def update_product_purchase_total(sender, instance, **kwargs):
    instance.purchase.calculate_total()

@receiver(post_save, sender=ServicePurchase)
def create_service_purchase_transaction(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            initiator=instance.store,
            store=instance.store,
            cashdesk=instance.cashdesk,
            type='debit',
            amount=instance.total,
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        )
    else:
        Transaction.objects.filter(
            content_type=ContentType.objects.get_for_model(instance),
            object_id=instance.id
        ).update(
            amount=instance.total,
            cashdesk=instance.cashdesk,
            store=instance.store,
            initiator=instance.store,
        )

# cashdesk balance manager

@receiver(post_save, sender=ClosingCashReceipt)
def update_balance_found_on_save(sender, instance, **kwargs):
    instance.update_cashdesk_closing()


@receiver(post_delete, sender=ClosingCashReceipt)
def update_balance_found_on_delete(sender, instance, **kwargs):
    instance.update_cashdesk_closing()

# inventory items creator

@receiver(post_save, sender=Inventory)
def create_inventory_items(sender, instance, created, **kwargs):
    stock = ProductStock.objects.all()
    if created:
        for obj in stock:
            InventoryItem.objects.create(inventory=instance, product_stock = obj)

# wallet balance manager

@receiver(post_save, sender=CashdeskClosing)
def update_wallet_balance_on_save(sender, instance, **kwargs):
    wallet = Wallet.objects.get(user=instance.initiator)
    wallet.balance += instance.difference
    wallet.save()
    print('cashdesk defficit')


@receiver(post_delete, sender=CashdeskClosing)
def update_wallet_balance_on_delete(sender, instance, **kwargs):
    wallet = Wallet.objects.get(user=instance.initiator)
    wallet.balance -= instance.difference
    wallet.save()
    print('cashdesk surplus')


# inventory stock manager
@receiver(post_save, sender=Inventory)
def create_stock_difference(sender, instance, **kwargs):
    initiator = instance.initiator
    store = instance.store
    items = instance.inventoryitem_set.all()

    stock_input = None
    stock_output = None
    
    # Iterate through inventory items and calculate the difference
    for item in items:
        quantity_difference = item.quantity_found - item.quantity_expected
        
        if quantity_difference > 0:
            print('surplus')
            # Create or update StockInput for excess inventory
            if not stock_input:
                stock_input = StockInput.objects.create(
                    initiator=initiator,
                    store=store,
                    type='difference',
                    description=f'''Difference d'inventaire {instance.id}'''
                )
            StockInputItem.objects.create(
                stock_input=stock_input,
                product_stock=item.product_stock,
                quantity=quantity_difference
            )
        elif quantity_difference < 0:
            print('defficit')
            # Create or update StockOutput for deficit inventory
            if not stock_output:
                stock_output = StockOutput.objects.create(
                    initiator=initiator,
                    store=store,
                    type='difference',
                    description=f"Difference d'inventaire {instance.id}"
                )
            StockOutputItem.objects.create(
                stock_output=stock_output,
                product_stock=item.product_stock,
                quantity=abs(quantity_difference)
            )
    
    # Calculate totals for stock input and output
    if stock_input:
        stock_input.calculate_total()
    if stock_output:
        stock_output.calculate_total()


@receiver(post_save, sender=InventoryItem)
def handle_inventory_item_save(sender, instance, **kwargs):
    initiator = instance.inventory.initiator
    store = instance.inventory.store

    quantity_difference = instance.quantity_found - instance.quantity_expected

    if quantity_difference != 0:
        stock_input = None
        stock_output = None

        if quantity_difference > 0:
            # Create StockInput for excess inventory
            stock_input, created = StockInput.objects.get_or_create(
                initiator=initiator,
                store=store,
                type='difference',
                description=f"Difference d'inventaire {instance.inventory.id}"
            )
            StockInputItem.objects.create(
                stock_input=stock_input,
                product_stock=instance.product_stock,
                quantity=quantity_difference
            )
            stock_input.calculate_total()
        elif quantity_difference < 0:
            # Create StockOutput for deficit inventory
            stock_output, created = StockOutput.objects.get_or_create(
                initiator=initiator,
                store=store,
                type='difference',
                description=f"Difference d'inventaire {instance.inventory.id}"
            )
            StockOutputItem.objects.create(
                stock_output=stock_output,
                product_stock=instance.product_stock,
                quantity=abs(quantity_difference)
            )
            stock_output.calculate_total()
