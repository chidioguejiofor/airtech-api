# Generated by Django 2.2 on 2019-04-08 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0013_auto_20190408_1450'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='createdBy',
            new_name='created_by',
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='updatedBy',
            new_name='updated_by',
        ),
    ]
