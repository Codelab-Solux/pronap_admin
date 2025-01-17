# Generated by Django 4.2 on 2024-07-07 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('base', '0018_remove_store_workers_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receivable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('label', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('due_date', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.client')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('initiator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.store')),
            ],
        ),
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('label', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('due_date', models.DateField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('initiator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.store')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.supplier')),
            ],
        ),
    ]
