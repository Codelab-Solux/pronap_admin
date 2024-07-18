# Generated by Django 4.2 on 2024-07-17 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0048_purchaseitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='product_stocks',
            field=models.ManyToManyField(blank=True, through='base.PurchaseItem', to='base.productstock'),
        ),
    ]
