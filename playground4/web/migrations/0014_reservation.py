# Generated by Django 4.2.3 on 2023-07-30 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_field_price_per_hour'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_working_day', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], default=1)),
                ('start_working_hour', models.IntegerField(choices=[(16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21)], default=16)),
                ('end_working_day', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], default=1)),
                ('end_working_hour', models.IntegerField(choices=[(16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21)], default=16)),
                ('reservation_date', models.DateField()),
                ('reservation_hour', models.IntegerField(choices=[(16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21)], default=16)),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.field')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
