# Generated by Django 4.2 on 2024-07-05 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_remove_client_sex_alter_client_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseitem',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='client',
            name='type',
            field=models.CharField(choices=[('company', 'Compagnie'), ('woman', 'Femme'), ('man', 'Homme')], default='company', max_length=50),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='type',
            field=models.CharField(choices=[('company', 'Compagnie'), ('woman', 'Femme'), ('man', 'Homme')], default='company', max_length=50),
        ),
    ]
