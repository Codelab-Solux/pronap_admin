from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Sale, SaleItem, ProductPurchase, PurchaseItem, ServicePurchase, Transaction
from django.contrib.contenttypes.models import ContentType

@receiver(post_save, sender=Sale)
def create_sale_transaction(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            initiator=instance.seller,
            store=instance.store,
            cashdesk=instance.cashdesk,
            type='credit',
            label='Achat de produit(s)',
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
            initiator=instance.seller,
        )

@receiver(post_save, sender=SaleItem)
def update_sale_total(sender, instance, created, **kwargs):
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
def update_product_purchase_total(sender, instance, created, **kwargs):
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
