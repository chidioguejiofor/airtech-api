# Generated by Django 2.2 on 2019-04-05 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0004_auto_20190404_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='schedule',
            field=models.DateTimeField(),
        ),
    ]
