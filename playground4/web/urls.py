from django.urls import path

from playground4.web import views
from playground4.web.views import FieldCreateView, FieldUpdateView, FieldDeleteView, ScheduleListView, \
	FieldScheduleView, ReviewListView, FieldOwnerReviews, \
	AddEventView, EventsListView, AllEventsListView, FieldDetailView, SignedUpEventsListView, cancel_sign_up, \
	change_password

urlpatterns=[
	path('register/', views.register, name='register'),
	path('login/success/', views.login_success, name='login_success'),
	path('login/', views.user_login, name='login'),
	path('', views.home, name='home'),
	path('logout/', views.user_logout, name='logout'),
	path('profile/', views.profile, name='profile'),
	path('profile/edit/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/delete/<int:pk>/', views.ProfileDeleteView.as_view(), name='profile_delete'),
	path('fields/add/', FieldCreateView.as_view(), name='add_field'),
    path('fields/<int:pk>/update/', FieldUpdateView.as_view(), name='update_field'),
    path('fields/<int:pk>/delete/', FieldDeleteView.as_view(), name='delete_field'),
	path('fields/', views.field_list, name='field_list'),
	path('fields/my/', views.my_fields, name='my_fields'),
	path('field_detail/<int:pk>/', FieldDetailView.as_view(), name='field_detail'),
	path('field/<int:pk>/reserve/', views.ReservationCreateView.as_view(), name='reservation_form'),
	path('reservation/<int:pk>/confirmation/', views.reservation_confirmation, name='reservation_confirmation'),
	path('schedule/', ScheduleListView.as_view(), name='schedule'),
	path('field/<int:field_id>/schedule/', FieldScheduleView.as_view(), name='field_schedule'),
	path('reservation/<int:pk>/cancel/', views.ReservationCancelView.as_view(), name='reservation_cancel'),
	path('field/<int:pk>/add_review/', views.AddReviewView.as_view(), name='add_review'),
	path('reviews/<int:pk>/', ReviewListView.as_view(), name='reviews'),
	path('reviews/field/<int:pk>/', FieldOwnerReviews.as_view(), name='field_owner_reviews'),
	path('add_event/<int:pk>/', AddEventView.as_view(), name='add_event'),
	path('events_list/<int:pk>/', EventsListView.as_view(), name='events_list'),
	path('all_events/', AllEventsListView.as_view(), name='all_events_list'),
	path('fields/<str:sport>/', views.FieldListBySportView.as_view(), name='field_list_by_sport'),
	path('event/<int:pk>/', views.event_detail, name='event_detail'),
	path('event/<int:pk>/registered-users/', views.registered_users_list, name='registered_users_list'),
	path('my-signed-up-events/', SignedUpEventsListView.as_view(), name='my_signed_up_events'),
	path('cancel-sign-up/<int:pk>/', cancel_sign_up, name='cancel_sign_up'),
	path('change-password/', change_password, name='change_password'),
]




# Wert789456
# Asdf4561