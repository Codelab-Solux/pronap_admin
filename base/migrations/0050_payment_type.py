# Generated by Django 4.2 on 2024-07-18 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0049_purchase_product_stocks'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='type',
            field=models.CharField(choices=[('credit', 'Encaissement'), ('debit', 'Décaissement')], default='credit', max_length=50),
            preserve_default=False,
        ),
    ]
