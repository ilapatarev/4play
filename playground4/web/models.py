from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from django.db import models
from django.conf import settings
from django.db.models import Avg
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class User(AbstractUser):
    SPORT_CHOICES = [
        ('Basketball', 'Basketball'),
        ('Football', 'Football'),
        ('Volleyball', 'Volleyball'),
        ('Tennis', 'Tennis'),
    ]

    username = models.CharField(validators=[MinLengthValidator(3)], max_length=150, unique=True, verbose_name='username')
    email = models.EmailField(unique=True, verbose_name='email')
    field_owner = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    image_url=models.URLField(blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    preferred_sport = models.CharField(max_length=100, choices=SPORT_CHOICES, blank=True)


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
    SPORT_CHOICES = [
        ('Basketball', 'Basketball'),
        ('Football', 'Football'),
        ('Volleyball', 'Volleyball'),
        ('Tennis', 'Tennis'),
    ]

    field_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    sport = models.CharField(max_length=100, choices=SPORT_CHOICES)
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

    def get_average_rating(self):
        average_rating = self.review_set.aggregate(Avg('rating'))['rating__avg']
        if average_rating:
            return round(average_rating, 1)
        return None

    def __str__(self):
        return self.name

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    reservation_hour = models.IntegerField(choices=[(hour, f'{hour}:00') for hour in range(16, 22)])

    def __str__(self):
        return f"Reservation for {self.field.name} by {self.user.username}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.field.name} by {self.user.username}"



class Event(models.Model):
    SPORT_CHOICES = [
        ('Basketball', 'Basketball'),
        ('Football', 'Football'),
        ('Volleyball', 'Volleyball'),
        ('Tennis', 'Tennis'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    sport = models.CharField(max_length=100, choices=SPORT_CHOICES)
    entry_fee=models.PositiveIntegerField(blank=False, default=0)
    event_date = models.DateTimeField(blank=False, default=timezone.now)
    slug = models.SlugField(unique=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug})

    max_sign_ups = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.title

class UserEventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
