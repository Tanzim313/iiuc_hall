# Create your models here.

from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {self.amount} Tk on {self.payment_date}"
