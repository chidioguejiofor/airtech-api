# Generated by Django 2.2 on 2019-04-15 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0015_auto_20190410_0400'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='currentPrice',
            new_name='current_price',
        ),
    ]