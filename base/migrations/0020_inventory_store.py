# Generated by Django 4.2 on 2024-07-07 15:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_receivable_debt'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.store'),
        ),
    ]
