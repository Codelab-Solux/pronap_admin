# Generated by Django 4.2 on 2024-07-18 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('base', '0050_payment_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='payment_option',
        ),
        migrations.AddField(
            model_name='stockoperation',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='stockoperation',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.payment'),
        ),
    ]
