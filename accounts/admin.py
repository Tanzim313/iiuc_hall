from django.contrib import admin

# Register your models here.
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'room_number', 'meal_serial')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'room_number')
    list_filter = ('room_number',)

    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = 'Student Name'

