from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .views import add_payment,edit_payment,payment_list,paid_students

urlpatterns = [
    path('submit/', views.submit_meal, name='meal'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manager/login/', auth_views.LoginView.as_view(template_name='meals/manager_login.html'), name='manager_login'),
    path('manager/logout/', auth_views.LogoutView.as_view(next_page='manager_login'), name='manager_logout'),
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    
    path('manager/daily_meal_list/', views.daily_meal_list, name='daily_meal_list'),
    path('manager/monthly-summary-pdf/', views.monthly_summary_pdf, name='monthly_summary_pdf'),
    path('manager/bazar-cost-update/', views.bazar_cost_update, name='bazar_cost_update'),
    path('manager/guest-meal-update/', views.guest_meal_update, name='guest_meal_update'),
    path('manager/payment-update/', views.payment_update, name='payment_update'),
    
    path('manager/info/', views.manager_info, name='manager_info'),
    path('manager/monthly-summary/', views.monthly_summary_page, name='monthly_summary_page'),
    path('manager/monthly-cost/', views.monthly_cost_page, name='monthly_cost_page'),
    
    path('meals/download/pdf/', views.download_daily_meal_pdf, name='download_daily_meal_pdf'),
    
    
    path('payments/', payment_list, name='payment_list'),
    path('payments/add/', add_payment, name='add_payment'),
    path('payments/edit/<int:payment_id>/', edit_payment, name='edit_payment'),
    path('payments/summary/',paid_students, name='payment_summary'),
    
    
    
    
]


from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




