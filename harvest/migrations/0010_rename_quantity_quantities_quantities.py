# Generated by Django 5.1.1 on 2025-01-04 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('harvest', '0009_booking_total_price_quantities'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quantities',
            old_name='quantity',
            new_name='quantities',
        ),
    ]
