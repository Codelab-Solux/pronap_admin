# base/management/commands/recalculate_cashdesk_balances.py
from django.core.management.base import BaseCommand
from base.models import *
from django.db.models import Sum


class Command(BaseCommand):
    help = 'Recalculate Cashdesk balances based on Transaction data'

    def handle(self, *args, **kwargs):
        cashdesks = Cashdesk.objects.all()
        for cashdesk in cashdesks:
            credits = Transaction.objects.filter(cashdesk=cashdesk, type='credit').aggregate(
                total=Sum('amount'))['total'] or 0
            debits = Transaction.objects.filter(cashdesk=cashdesk, type='debit').aggregate(
                total=Sum('amount'))['total'] or 0
            cashdesk.credits = credits
            cashdesk.debits = debits
            cashdesk.balance = credits - debits
            cashdesk.save()
            self.stdout.write(self.style.SUCCESS(
                f'Recalculated balances for Cashdesk {cashdesk.id}'))
