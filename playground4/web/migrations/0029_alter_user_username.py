# Generated by Django 4.2.3 on 2023-08-10 15:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0028_event_event_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='username'),
        ),
    ]
