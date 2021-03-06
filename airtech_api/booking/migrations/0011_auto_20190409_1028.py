# Generated by Django 2.2 on 2019-04-09 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0014_auto_20190408_1510'),
        ('users', '0007_auto_20190408_1436'),
        ('booking', '0010_auto_20190409_0936'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='flight',
            new_name='flight_id',
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('flight_id', 'created_by')},
        ),
    ]
