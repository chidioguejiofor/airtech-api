# Generated by Django 2.2 on 2019-04-09 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0009_auto_20190409_0928'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='expiryDate',
            new_name='expiry_date',
        ),
    ]
