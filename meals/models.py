from django.db import models
from django.contrib.auth.models import User

class DiningRepresentative(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dining_profile')
    department = models.CharField(max_length=100)
    room_number = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    meal_serial = models.IntegerField()
    photo = models.ImageField(upload_to='dining_representatives/')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.user.get_full_name()


class MealManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='meal_manager_profile')
    department = models.CharField(max_length=100)
    room_number = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)
    meal_serial = models.IntegerField()
    photo = models.ImageField(upload_to='meal_managers/')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.user.get_full_name()



class Meal(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    

    class Meta:
        unique_together = ('student', 'date')
        
        

