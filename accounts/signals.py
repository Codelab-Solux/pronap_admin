from django.db.models.signals import post_migrate, post_save, pre_delete, pre_save
from django.dispatch import receiver
from django.apps import apps
from .models import *


@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    if sender.name == 'accounts':
        if not Role.objects.filter(name='Administrateur').exists():
            Role.objects.create(
                name='Administrateur', description='Administrator Role', sec_level=3)
        if not Role.objects.filter(name='Gestionaire').exists():
            Role.objects.create(
                name='Gestionaire', description='Manager Role', sec_level=2)
        if not Role.objects.filter(name='Employé').exists():
            Role.objects.create(
                name='Employé', description='Staff Role', sec_level=1)


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def create_or_update_wallet(sender, instance, **kwargs):
    if not hasattr(instance, 'wallet'):
        Wallet.objects.create(user=instance, balance=0)

