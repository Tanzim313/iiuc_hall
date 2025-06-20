from django.db import models
from django.contrib.auth.models import User


# Create your models here.
# accounts/models.py

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    meal_serial = models.IntegerField()
    

    
    def __str__(self):
        return self.user.get_full_name()
    class Meta:
        ordering = ['meal_serial']  # Default ordering by meal_serial ascending


