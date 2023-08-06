from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import User, Field, Event, Review, Reservation


class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'sport', 'price_per_hour', 'field_owner')
    list_filter = ('sport', 'price_per_hour', 'field_owner', 'location')
    ordering = ('name',)
    search_fields = ('name', 'location')

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'field_owner')
    list_filter = ('age', 'groups')
    ordering = ('username',)
    search_fields = ('name', 'location')



class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published',  'sport')
    list_filter = ('sport',)
    ordering = ('-date_published',)
    search_fields = ('name', 'location')
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'field',  'reservation_date')
    list_filter = ('user', 'field')
    ordering = ('-reservation_date',)
    search_fields = ('user', 'field')
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'field',  'created_at')
    list_filter = ('field', 'user')
    ordering = ('-created_at',)
    search_fields = ('user', 'field')




admin.site.register(Field, FieldAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Reservation, ReservationAdmin)

admin.site.register(Event, EventAdmin)

admin.site.register(User, UserAdmin)