# Generated by Django 2.2.2 on 2019-06-29 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0020_auto_20190626_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='paid_at',
            field=models.DateTimeField(null=True),
        ),
    ]