
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Field, Reservation, Review, Event


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)
    field_owner = forms.BooleanField(required=False)


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'field_owner')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].help_text = None
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters. Your password can’t be a commonly used password. Your password can’t be entirely numeric.'
        self.fields['password2'].help_text = None
        self.fields['field_owner'].help_text = 'Check here if You want to offer your field'
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['name', 'location', 'sport', 'description', 'image_url', 'start_working_day', 'start_working_hour', 'end_working_day', 'end_working_hour']


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['reservation_date', 'reservation_hour']
        widgets = {
            'reservation_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'category', 'content', 'image']

