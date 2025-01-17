# Generated by Django 4.2 on 2024-07-17 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0045_debt_is_fully_paid_productstock_lot_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('input', 'Entrée'), ('output', 'Sortie')], default='input', max_length=10)),
                ('subtype', models.CharField(choices=[('purchase', 'Achat'), ('return', 'Retour'), ('transfer', 'Transfer'), ('difference', 'Difference d’inventaire'), ('gift', 'Cadeau'), ('sale', 'Vente'), ('usage', 'Utilisation interne'), ('don', 'Don')], max_length=50)),
                ('items', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('initiator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StockOperationItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('product_stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.productstock')),
                ('stock_operation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.stockoperation')),
            ],
        ),
        migrations.RemoveField(
            model_name='stockinputitem',
            name='product_stock',
        ),
        migrations.RemoveField(
            model_name='stockinputitem',
            name='stock_input',
        ),
        migrations.RemoveField(
            model_name='stockoutput',
            name='initiator',
        ),
        migrations.RemoveField(
            model_name='stockoutput',
            name='product_stocks',
        ),
        migrations.RemoveField(
            model_name='stockoutput',
            name='store',
        ),
        migrations.RemoveField(
            model_name='stockoutputitem',
            name='product_stock',
        ),
        migrations.RemoveField(
            model_name='stockoutputitem',
            name='stock_output',
        ),
        migrations.DeleteModel(
            name='StockInput',
        ),
        migrations.DeleteModel(
            name='StockInputItem',
        ),
        migrations.DeleteModel(
            name='StockOutput',
        ),
        migrations.DeleteModel(
            name='StockOutputItem',
        ),
        migrations.AddField(
            model_name='stockoperation',
            name='product_stocks',
            field=models.ManyToManyField(through='base.StockOperationItem', to='base.productstock'),
        ),
        migrations.AddField(
            model_name='stockoperation',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.store'),
        ),
    ]
