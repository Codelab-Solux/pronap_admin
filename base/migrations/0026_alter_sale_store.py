# Generated by Django 4.2 on 2024-07-09 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_rename_observation_productpurchase_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='store',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.store'),
        ),
    ]