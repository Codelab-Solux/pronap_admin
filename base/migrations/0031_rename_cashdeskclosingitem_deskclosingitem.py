# Generated by Django 4.2 on 2024-07-09 22:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_payment_content_type_payment_object_id'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CashdeskClosingItem',
            new_name='DeskClosingItem',
        ),
    ]
