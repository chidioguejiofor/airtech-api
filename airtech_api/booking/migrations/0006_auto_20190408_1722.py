# Generated by Django 2.2 on 2019-04-08 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20190408_1436'),
        ('flight', '0014_auto_20190408_1510'),
        ('booking', '0005_auto_20190408_1644'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('flight_id', 'created_by')},
        ),
    ]
