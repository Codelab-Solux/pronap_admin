import logging
from django.core.management.base import BaseCommand
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from base.models import *


class Command(BaseCommand):
    help = 'Recalculate product stock quantities based on purchase and sale items.'

    def handle(self, *args, **kwargs):
        logger = logging.getLogger('stock_recalculation')
        handler = logging.FileHandler('stock_recalculation.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        logger.info('Starting stock recalculation...')

        # Update product stock quantities
        for product_stock in ProductStock.objects.all():
            total_purchased = PurchaseItem.objects.filter(
                product_stock=product_stock).aggregate(total=Sum('quantity'))['total'] or 0
            total_sold = SaleItem.objects.filter(
                product_stock=product_stock).aggregate(total=Sum('quantity'))['total'] or 0
            total_quantity = total_purchased - total_sold
            product_stock.quantity = total_quantity
            product_stock.save()

            logger.debug(
                f'Updated {product_stock} to quantity {total_quantity}')
            self.stdout.write(self.style.SUCCESS(
                f'Updated {product_stock} to quantity {total_quantity}'))

        # Update stock operations for purchases
        for purchase in Purchase.objects.all():
            stock_operation, created = StockOperation.objects.get_or_create(
                content_type=ContentType.objects.get_for_model(purchase),
                object_id=purchase.id,
                defaults={
                    'type': 'input',
                    'subtype': 'purchase',
                    'store': purchase.store,
                    'initiator': purchase.initiator
                }
            )
            total_quantity = PurchaseItem.objects.filter(
                purchase=purchase).aggregate(total=Sum('quantity'))['total'] or 0
            stock_operation.total = total_quantity
            stock_operation.save()

            if created:
                logger.debug(
                    f'Created stock operation for purchase {purchase.id}')
                self.stdout.write(self.style.SUCCESS(
                    f'Created stock operation for purchase {purchase.id}'))
            else:
                logger.debug(
                    f'Updated stock operation for purchase {purchase.id}')
                self.stdout.write(self.style.SUCCESS(
                    f'Updated stock operation for purchase {purchase.id}'))

        # Update stock operations for sales
        for sale in Sale.objects.all():
            stock_operation, created = StockOperation.objects.get_or_create(
                content_type=ContentType.objects.get_for_model(sale),
                object_id=sale.id,
                defaults={
                    'type': 'output',
                    'subtype': 'sale',
                    'store': sale.store,
                    'initiator': sale.initiator
                }
            )
            total_quantity = SaleItem.objects.filter(
                sale=sale).aggregate(total=Sum('quantity'))['total'] or 0
            stock_operation.total = total_quantity
            stock_operation.save()

            if created:
                logger.debug(f'Created stock operation for sale {sale.id}')
                self.stdout.write(self.style.SUCCESS(
                    f'Created stock operation for sale {sale.id}'))
            else:
                logger.debug(f'Updated stock operation for sale {sale.id}')
                self.stdout.write(self.style.SUCCESS(
                    f'Updated stock operation for sale {sale.id}'))

        logger.info('Stock recalculation complete.')
        self.stdout.write(self.style.SUCCESS(
            'Product stock recalculations complete.'))
