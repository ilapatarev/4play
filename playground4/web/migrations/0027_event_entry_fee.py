# Generated by Django 4.2.3 on 2023-08-06 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0026_usereventregistration'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='entry_fee',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
