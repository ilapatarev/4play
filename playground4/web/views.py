from django import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.views import View
from .forms import LoginForm, RegistrationForm, ReservationForm, ReviewForm, EventForm
from .models import User, Field, Reservation, Review, Event
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
    fields = ['name', 'location', 'sport', 'description', 'image_url', 'start_working_day', 'start_working_hour', 'end_working_day', 'end_working_hour', 'price_per_hour']
    success_url = reverse_lazy('my_fields')

    def form_valid(self, form):
        form.instance.field_owner = self.request.user
        return super().form_valid(form)



class FieldUpdateView(LoginRequiredMixin, UpdateView):
    model = Field
    template_name = 'field/update_field.html'
    fields = ['name', 'location', 'sport', 'description', 'image_url', 'start_working_day', 'start_working_hour', 'end_working_day', 'end_working_hour', 'price_per_hour']
    success_url = reverse_lazy('my_fields')

    def get_queryset(self):
        return Field.objects.filter(field_owner=self.request.user)


class FieldDeleteView(LoginRequiredMixin, DeleteView):
    model = Field
    template_name = 'field/delete_field.html'
    success_url = reverse_lazy('my_fields')

    def get_queryset(self):
        return Field.objects.filter(field_owner=self.request.user)

class FieldDetailView(View):
    template_name = 'field/field_detail.html'
    login_url = 'login'

    def get(self, request, pk):
        field = get_object_or_404(Field, pk=pk)

        # Check if the user is authenticated
        is_authenticated = request.user.is_authenticated

        # Check if the user has already reviewed the field
        has_reviewed = False
        review_form = ReviewForm()

        if is_authenticated:
            has_reviewed = Review.objects.filter(user=request.user, field=field).exists()
        else:
            # If the user is anonymous, hide the review form
            review_form = None

        context = {
            'field': field,
            'review_form': review_form,
            'has_reviewed': has_reviewed,
            'is_authenticated': is_authenticated,
            'field_owner': field.field_owner,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        field = get_object_or_404(Field, pk=pk)

        # Check if the user is authenticated
        is_authenticated = request.user.is_authenticated

        # If the user is anonymous, do not process the review form submission
        if not is_authenticated:
            messages.error(request, "You need to log in to add a review.")
            return HttpResponseRedirect(reverse_lazy('field_detail', kwargs={'pk': pk}))

        review_form = ReviewForm(request.POST)

        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.field = field
            review.save()
            messages.success(request, "Review successfully added.")
        else:
            messages.error(request, "Failed to add the review. Please try again.")

        return HttpResponseRedirect(reverse_lazy('field_detail', kwargs={'pk': pk}))

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        field_id = self.kwargs['field_id']
        field = get_object_or_404(Field, pk=field_id)
        context['field'] = field
        return context

class ReservationCancelView(View):
    def post(self, request, pk):
        # Get the reservation object
        reservation = Reservation.objects.get(pk=pk)

        # Check if the reservation belongs to the current user
        if reservation.user == request.user:
            # Delete the reservation
            reservation.delete()

            # Display a success message
            messages.success(request, "Reservation successfully canceled.")
        else:
            # Display an error message if the reservation doesn't belong to the user
            messages.error(request, "You are not authorized to cancel this reservation.")

        # Redirect to the schedule page
        return redirect('schedule')

class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    template_name = 'review/add_review.html'
    form_class = ReviewForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        field = get_object_or_404(Field, pk=self.kwargs['pk'])
        form.instance.field = field
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Review successfully added.")
        return reverse_lazy('field_detail', kwargs={'pk': self.kwargs['pk']})


class ReviewListView(View):
    template_name = 'review/reviews.html'

    def get(self, request, pk):
        field = get_object_or_404(Field, pk=pk)
        reviews = Review.objects.filter(field=field)

        return render(request, self.template_name, {'field': field, 'reviews': reviews})

class FieldOwnerReviews(View):
    template_name = 'review/field_owner_reviews.html'

    def get(self, request, pk):
        field = get_object_or_404(Field, pk=pk)
        reviews = Review.objects.filter(field=field)

        return render(request, self.template_name, {'field': field, 'reviews': reviews})


class EventsListView(View):
    template_name = 'events/events_list.html'

    def get(self, request, pk):
        field = get_object_or_404(Field, pk=pk)
        events_list = Event.objects.filter(field=field)
        return render(request, self.template_name, {'field': field, 'events_list': events_list})


class AddEventView(View):
    template_name = 'events/add_event.html'

    def get(self, request, pk):
        field = get_object_or_404(Field, pk=pk)
        form = EventForm()
        return render(request, self.template_name, {'form': form, 'field': field})

    def post(self, request, pk):
        field = get_object_or_404(Field, pk=pk)
        form = EventForm(request.POST, request.FILES)

        if form.is_valid():
            events = form.save(commit=False)
            events.author = request.user
            events.field = field
            events.save()
            return redirect('events_list', pk=pk)

        return render(request, self.template_name, {'form': form, 'field': field})

class AllEventsListView(ListView):
    model = Event
    template_name = 'events/all_events_list.html'
    context_object_name = 'events_list'
    ordering = ['-date_published']  # Order events by date_published in descending order

    def get_queryset(self):
        return super().get_queryset().select_related('field')

class FieldListBySportView(View):
    template_name = 'field/field_list_by_sport.html'

    def get(self, request, sport=None):
        if sport:
            fields = Field.objects.filter(sport__iexact=sport)
        else:
            fields = Field.objects.all()

        context = {
            'fields': fields,
            'selected_sport': sport,  # To highlight the selected sport in the template
        }

        return render(request, self.template_name, context)




