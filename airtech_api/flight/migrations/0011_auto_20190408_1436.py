# Generated by Django 2.2 on 2019-04-08 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0010_auto_20190408_1435'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flight',
            old_name='createdAt',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='flight',
            old_name='updatedAt',
            new_name='updated_at',
        ),
    ]