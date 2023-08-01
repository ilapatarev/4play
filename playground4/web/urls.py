from django.urls import path

from playground4.web import views
from playground4.web.views import FieldCreateView, FieldUpdateView, FieldDeleteView, ScheduleListView, \
	FieldScheduleView, ReviewListView, FieldOwnerReviews, NewsListView, AddNewsView, AllNewsView

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
	path('fields/<int:pk>/', views.FieldDetailView.as_view(), name='field_detail'),
	path('field/<int:pk>/reserve/', views.ReservationCreateView.as_view(), name='reservation_form'),
	path('reservation/<int:pk>/confirmation/', views.reservation_confirmation, name='reservation_confirmation'),
	path('schedule/', ScheduleListView.as_view(), name='schedule'),
	path('field/<int:field_id>/schedule/', FieldScheduleView.as_view(), name='field_schedule'),
	path('reservation/<int:pk>/cancel/', views.ReservationCancelView.as_view(), name='reservation_cancel'),
	path('field/<int:pk>/add_review/', views.AddReviewView.as_view(), name='add_review'),
	path('reviews/<int:pk>/', ReviewListView.as_view(), name='reviews'),
	path('reviews/field/<int:pk>/', FieldOwnerReviews.as_view(), name='field_owner_reviews'),
	path('add_news/<int:pk>/', AddNewsView.as_view(), name='add_news'),
	path('news_list/<int:pk>/', NewsListView.as_view(), name='news_list'),
	path('news/', AllNewsView.as_view(), name='all_news_list'),
]

# Wert789456