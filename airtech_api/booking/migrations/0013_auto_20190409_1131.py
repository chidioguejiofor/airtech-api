# Generated by Django 2.2 on 2019-04-09 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0012_auto_20190409_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='flight_id',
            field=models.CharField(default=None, max_length=10000),
            preserve_default=False,
        ),
    ]