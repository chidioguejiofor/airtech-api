# Generated by Django 2.2 on 2019-04-05 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0006_auto_20190405_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='createdBy',
            field=models.ForeignKey(
                db_column='createdBy',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='creator',
                to='users.User'),
        ),
    ]
