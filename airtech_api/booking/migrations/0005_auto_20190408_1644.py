# Generated by Django 2.2 on 2019-04-08 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20190408_1641'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='flight',
            new_name='flight_id',
        ),
    ]
