# Generated by Django 4.2.3 on 2023-07-29 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]
