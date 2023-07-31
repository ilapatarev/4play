from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.views.generic import DetailView
from .forms import LoginForm, RegistrationForm, ReservationForm
from .models import User, Field, Reservation
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import ListView


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for registering. You can now login.')
            return redirect('login_success')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_success(request):
    # Display a success message to the user
    return render(request, 'login_success.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect(request.GET.get('next', 'home'))  # Redirect to the home page after successful login
            else:

               messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile/profile.html', {'profile': user})


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'profile/profile_edit.html'
    fields = ['first_name', 'last_name', 'age', 'phone', 'username', 'image_url', 'preferred_sport', 'company_name']  # Include other fields if needed

    def get_success_url(self):
        return reverse_lazy('profile')

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'profile/profile_confirm_delete.html'
    success_url = reverse_lazy('home')

# views.py



def field_list(request):
    fields = Field.objects.all()
    return render(request, 'field/field_list.html', {'fields': fields})


@login_required
def my_fields(request):
    fields = Field.objects.filter(field_owner=request.user)
    return render(request, 'field/my_fields.html', {'fields': fields})



class FieldCreateView(LoginRequiredMixin, CreateView):
    model = Field
    template_name = 'field/add_field.html'
    fields = ['name', 'location', 'sport', 'description', 'image_url', 'start_working_day', 'start_working_hour', 'end_working_day', 'end_working_hour']
    success_url = reverse_lazy('my_fields')

    def form_valid(self, form):
        form.instance.field_owner = self.request.user
        return super().form_valid(form)



class FieldUpdateView(LoginRequiredMixin, UpdateView):
    model = Field
    template_name = 'field/update_field.html'
    fields = ['name', 'location', 'sport', 'description', 'image_url', 'start_working_day', 'start_working_hour', 'end_working_day', 'end_working_hour']
    success_url = reverse_lazy('my_fields')

    def get_queryset(self):
        return Field.objects.filter(field_owner=self.request.user)


class FieldDeleteView(LoginRequiredMixin, DeleteView):
    model = Field
    template_name = 'field/delete_field.html'
    success_url = reverse_lazy('my_fields')

    def get_queryset(self):
        return Field.objects.filter(field_owner=self.request.user)

class FieldDetailView(DetailView):
    model = Field
    template_name = 'field/field_detail.html'
    context_object_name = 'field'


class ReservationCreateView(CreateView):
    model = Reservation
    template_name = 'reservation/reservation_form.html'
    form_class = ReservationForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.field = get_object_or_404(Field, pk=self.kwargs['pk'])

        # Access the selected reservation date and hour
        reservation_date = form.cleaned_data.get('reservation_date')
        reservation_hour = form.cleaned_data.get('reservation_hour')

        if reservation_date and reservation_hour:
            field = get_object_or_404(Field, pk=self.kwargs['pk'])
            start_working_day = field.start_working_day
            start_working_hour = field.start_working_hour
            end_working_day = field.end_working_day
            end_working_hour = field.end_working_hour

            # Check if the selected reservation date and hour are within the working hours
            if reservation_date.weekday() + 1 < start_working_day or reservation_date.weekday() + 1 > end_working_day:
                form.add_error('reservation_date', "Reservations are only allowed on working days.")
            elif reservation_hour < start_working_hour or reservation_hour > end_working_hour:
                form.add_error('reservation_hour', "Reservations are only allowed during working hours.")
            else:
                # Check for duplicate reservations
                existing_reservations = Reservation.objects.filter(
                    field=field,
                    reservation_date=reservation_date,
                    reservation_hour=reservation_hour
                )

                if existing_reservations.exists():
                    form.add_error(None, "This hour is already reserved for the selected date.")
                else:
                    messages.success(self.request, "Reservation successfully created.")
                    return super().form_valid(form)

        return super().form_invalid(form)

    def get_success_url(self):
        # Redirect to the confirmation page upon successful reservation
        return reverse_lazy('reservation_confirmation', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        field = get_object_or_404(Field, pk=self.kwargs['pk'])
        context['field_name'] = field.name
        context['start_working_day'] = field.get_start_working_day_display()
        context['start_working_hour'] = field.start_working_hour
        context['end_working_day'] = field.get_end_working_day_display()
        context['end_working_hour'] = field.end_working_hour
        return context

def reservation_confirmation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'reservation/reservation_confirmation.html', {'reservation': reservation})



class ScheduleListView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservation/schedule_list.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        # Only display reservations for the current user, ordered by reservation date and hour
        return Reservation.objects.filter(user=self.request.user).order_by('reservation_date', 'reservation_hour')

    # views.py


class FieldScheduleView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = 'reservation/field_schedule.html'
    context_object_name = 'reservations'
    ordering = ['reservation_date', 'reservation_hour']

    def get_queryset(self):
        field_id = self.kwargs['field_id']
        return Reservation.objects.filter(field_id=field_id)


