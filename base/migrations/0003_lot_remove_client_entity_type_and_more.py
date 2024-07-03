# Generated by Django 4.2 on 2024-07-02 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_cashdesk_store_alter_product_store_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='client',
            name='entity_type',
        ),
        migrations.RemoveField(
            model_name='supplier',
            name='entity_type',
        ),
        migrations.AddField(
            model_name='client',
            name='type',
            field=models.CharField(choices=[('person', 'Personne'), ('company', 'Compagnie')], default='company', max_length=50),
        ),
        migrations.AddField(
            model_name='supplier',
            name='type',
            field=models.CharField(choices=[('person', 'Personne'), ('company', 'Compagnie')], default='company', max_length=50),
            preserve_default=False,
        ),
    ]