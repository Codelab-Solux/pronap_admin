# Generated by Django 4.2 on 2024-07-24 14:07

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0060_alter_productstock_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, default='', max_length=255, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='debt',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='debt',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='product',
            name='unit',
        ),
        migrations.RemoveField(
            model_name='receivable',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='receivable',
            name='object_id',
        ),
        migrations.AlterField(
            model_name='cashdeskclosing',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='client',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='closingcashreceipt',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='debt',
            name='purchase',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='base.purchase'),
        ),
        migrations.AlterField(
            model_name='debt',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='family',
            name='name',
            field=models.CharField(blank=True, db_index=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='date',
            field=models.DateField(db_index=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='lot',
            name='name',
            field=models.CharField(blank=True, db_index=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='lot',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='product',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='productstock',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='product_stocks',
            field=models.ManyToManyField(blank=True, db_index=True, through='base.PurchaseItem', to='base.productstock'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='purchaseitem',
            name='product_stock',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='base.productstock'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='receivable',
            name='sale',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='base.sale'),
        ),
        migrations.AlterField(
            model_name='receivable',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='sale',
            name='product_stocks',
            field=models.ManyToManyField(db_index=True, through='base.SaleItem', to='base.productstock'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='product_stock',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to='base.productstock'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='sale',
            field=models.ForeignKey(default=60, on_delete=django.db.models.deletion.CASCADE, to='base.sale'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stockoperation',
            name='product_stocks',
            field=models.ManyToManyField(db_index=True, through='base.StockOperationItem', to='base.productstock'),
        ),
        migrations.AlterField(
            model_name='stockoperation',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='stockoperationitem',
            name='stock_operation',
            field=models.ForeignKey(default=69, on_delete=django.db.models.deletion.CASCADE, to='base.stockoperation'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='store',
            name='name',
            field=models.CharField(blank=True, db_index=True, default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='timestamp',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
    ]
