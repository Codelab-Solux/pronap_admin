# Generated by Django 4.2 on 2024-07-08 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_inventory_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debt',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='receivable',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
