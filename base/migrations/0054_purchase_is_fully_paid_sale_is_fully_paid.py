# Generated by Django 4.2 on 2024-07-19 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0053_alter_purchase_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='is_fully_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sale',
            name='is_fully_paid',
            field=models.BooleanField(default=False),
        ),
    ]
