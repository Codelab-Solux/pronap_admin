# Generated by Django 4.2 on 2024-07-21 16:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0058_remove_purchase_amount_debt_is_fully_paid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='debt',
            name='purchase',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='base.purchase'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='productstock',
            name='price',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='productstock',
            name='promo_price',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='productstock',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
