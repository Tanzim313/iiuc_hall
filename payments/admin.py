from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'is_paid', 'payment_date')
    list_filter = ('is_paid', 'payment_date')
    search_fields = ('student__username',)
