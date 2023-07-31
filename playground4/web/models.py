
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name='username')
    email = models.EmailField(unique=True, verbose_name='email')
    field_owner = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    image_url=models.URLField(blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    preferred_sport = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Field(models.Model):
    DAY_CHOICES = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]

    field_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    sport = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(blank=True)
    price_per_hour=models.PositiveIntegerField(blank=False, default=0)

    # Start working day of the week (choices: 1-7, representing Monday-Sunday)
    start_working_day = models.IntegerField(choices=DAY_CHOICES, default=1)

    # Start working hour (choices: 16-21)
    start_working_hour = models.IntegerField(choices=[(hour, hour) for hour in range(16, 22)], default=16)

    # End working day of the week (choices: 1-7, representing Monday-Sunday)
    end_working_day = models.IntegerField(choices=DAY_CHOICES, default=1)

    # End working hour (choices: 16-21)
    end_working_hour = models.IntegerField(choices=[(hour, hour) for hour in range(16, 22)], default=16)

    def get_start_working_day(self):
        return dict(self.DAY_CHOICES)[self.start_working_day]

    def get_end_working_day(self):
        return dict(self.DAY_CHOICES)[self.end_working_day]

    def get_start_working_hour(self):
        return f"{self.start_working_hour}:00"

    def get_end_working_hour(self):
        return f"{self.end_working_hour}:00"

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    reservation_hour = models.IntegerField(choices=[(hour, f'{hour}:00') for hour in range(16, 22)])

    def __str__(self):
        return f"Reservation for {self.field.name} by {self.user.username}"


