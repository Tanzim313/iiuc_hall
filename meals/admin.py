# admin.py
from django.contrib import admin
from django.contrib.auth.models import User

#admin.site.register(User)  # ekhane meal manager er user create korbe admin

from .models import MealManager, DiningRepresentative

@admin.register(MealManager)
class MealManagerAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'room_number', 'phone_number', 'meal_serial', 'start_date', 'end_date')
    search_fields = ('user', 'department', 'phone_number')

@admin.register(DiningRepresentative)
class DiningRepresentativeAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'room_number', 'phone_number', 'meal_serial', 'start_date', 'end_date')
    search_fields = ('user', 'department', 'phone_number')
