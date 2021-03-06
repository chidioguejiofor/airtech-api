# Generated by Django 2.2.1 on 2019-05-24 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image_public_id',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.URLField(null=True),
        ),
    ]
