# Generated by Django 4.2 on 2024-07-05 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_stockinput_store_stockoutput_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='supplier',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]