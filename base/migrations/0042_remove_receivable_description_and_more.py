# Generated by Django 4.2 on 2024-07-15 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0041_remove_transaction_cashdesk_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receivable',
            name='description',
        ),
        migrations.RemoveField(
            model_name='receivable',
            name='initiator',
        ),
        migrations.RemoveField(
            model_name='receivable',
            name='store',
        ),
        migrations.AddField(
            model_name='receivable',
            name='sale',
            field=models.ForeignKey(default=43, on_delete=django.db.models.deletion.CASCADE, to='base.sale'),
            preserve_default=False,
        ),
    ]