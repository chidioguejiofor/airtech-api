# Generated by Django 2.2 on 2019-04-06 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0007_auto_20190405_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='createdAt',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='flight',
            name='updatedAt',
            field=models.DateTimeField(),
        ),
    ]
