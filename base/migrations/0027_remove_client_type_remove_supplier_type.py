# Generated by Django 4.2 on 2024-07-09 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0026_alter_sale_store'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='type',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='type',
        ),
    ]