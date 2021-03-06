# Generated by Django 2.1.7 on 2019-03-28 16:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now_add=True)),
                ('id',
                 models.UUIDField(default=uuid.uuid4,
                                  editable=False,
                                  primary_key=True,
                                  serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('gender',
                 models.CharField(choices=[('M', 'Male'), ('F', 'Female')],
                                  max_length=1)),
                ('date_of_birth', models.DateField(null=True)),
                ('username', models.CharField(max_length=50)),
                ('password_hash', models.TextField()),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
