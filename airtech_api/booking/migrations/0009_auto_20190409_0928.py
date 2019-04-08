# Generated by Django 2.2 on 2019-04-09 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0014_auto_20190408_1510'),
        ('users', '0007_auto_20190408_1436'),
        ('booking', '0008_auto_20190409_0925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='flight_id',
            new_name='flight',
        ),
        migrations.AlterUniqueTogether(
            name='booking',
            unique_together={('flight', 'created_by')},
        ),
    ]