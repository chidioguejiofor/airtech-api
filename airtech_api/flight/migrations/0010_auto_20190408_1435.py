# Generated by Django 2.2 on 2019-04-08 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0009_auto_20190406_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='createdBy',
            field=models.ForeignKey(
                db_column='create_by',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='creator',
                to='users.User'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='updatedBy',
            field=models.ForeignKey(
                db_column='updated_by',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='updater',
                to='users.User'),
        ),
    ]