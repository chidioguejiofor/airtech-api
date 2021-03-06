# Generated by Django 2.2.3 on 2019-07-06 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0023_auto_20190704_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='created_by',
            field=models.ForeignKey(
                db_column='created_by',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='bookings',
                to='users.User'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='flight_model',
            field=models.ForeignKey(
                db_column='flight_id',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='bookings',
                to='flight.Flight'),
        ),
    ]
