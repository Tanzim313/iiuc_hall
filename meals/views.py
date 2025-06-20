# views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime,timedelta
from .models import DiningRepresentative, Meal, MealManager
from payments.models import Payment
from django.db.models import Sum
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
import pytz
from django.template.loader import render_to_string
from payments.forms import PaymentForm
#from weasyprint import HTML






from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from .models import Meal
import io


def daily_meal_list(request):
    today = timezone.now().date()
    meals = Meal.objects.filter(date=today).select_related('student__studentprofile').order_by('student__studentprofile__meal_serial')

    context = {
        'meals': meals,
        'date': today,
    }
    return render(request, 'meals/daily_meal_list.html', context)


def monthly_summary_pdf(request):
    return HttpResponse("Monthly summary PDF will be generated.")

def bazar_cost_update(request):
    return HttpResponse("Bazar cost update form.")

def guest_meal_update(request):
    return HttpResponse("Guest meal update form.")

def payment_update(request):
    return HttpResponse("Payment input form.")



#meal manager dashboard:
@staff_member_required
def manager_dashboard(request):
    return render(request,'meals/manager_dashboard.html')

def manager_info(request):
    now = timezone.now().date()

    # DiningRepresentative, MealManager

    # ২ jon dining representative (6 month expaired date)
    six_months_ago = now - timedelta(days=30*6)
    dr_list = DiningRepresentative.objects.filter(
        start_date__lte=now,
        end_date__gte=now
    )[:2]  

    # ২ jon meal manager (15 din expaired date)
    mm_list = MealManager.objects.filter(
        start_date__lte=now,
        end_date__gte=now
    )[:2]

    context = {
        'dr1': dr_list[0] if len(dr_list) > 0 else None,
        'dr2': dr_list[1] if len(dr_list) > 1 else None,
        'mm1': mm_list[0] if len(mm_list) > 0 else None,
        'mm2': mm_list[1] if len(mm_list) > 1 else None,
    }

    return render(request, 'meals/manager_info.html', context)


def monthly_summary_page(request):
    # ekane query kore summary boshate hobe future a
    return render(request, 'meals/monthly_summary_page.html')

def monthly_cost_page(request):
    # ekane individual student er meal cost boshate hobe future a
    return render(request, 'meals/monthly_cost_page.html')



#studnet dashboard:
@login_required
def dashboard(request):
    meals = Meal.objects.filter(student=request.user).order_by('-date')
    
    total_paid = Payment.objects.filter(student=request.user, is_paid=True).aggregate(Sum('amount'))['amount__sum'] or 0

    
    return render(request, 'meals/dashboard.html', {
        'meals': meals,
        'total_paid': total_paid,
    })

@login_required
def submit_meal(request):
    today = datetime.now().date()   
    now = datetime.now().time()

    if request.method == 'POST':
        date_str = request.POST.get('date')
        try:
            meal_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            messages.error(request, "Invalid date format.")
            return redirect('dashboard')
        breakfast = request.POST.get('breakfast') == 'on'
        lunch = request.POST.get('lunch') == 'on'
        dinner = request.POST.get('dinner') == 'on'

        # ✅ Payment Rules
        payments = Payment.objects.filter(student=request.user, is_paid=True)
        total_paid = sum(p.amount for p in payments if p.payment_date.month == meal_date.month)

        # Rule 1:  6:00 Am (Today's meal after 6 AM disallow)
        if meal_date == today and now.hour >= 6:
            messages.error(request, "You cannot submit today's meal after 6:00 AM.")
            return redirect('dashboard')

        # Rule 2: ৩  Meal Off (No payment, meals off within 3 days)
        if not payments.exists() and (meal_date - today).days <= 3:
            messages.error(request, "You must pay within 3 days to activate meals.")
            return redirect('dashboard')

        # Rule 3: ১৫ -- ৫০০ --Meal Off (If after 15th, pay at least 500 tk)
        if meal_date.day > 15 and total_paid < 500:
            messages.error(request, "You must pay at least 500tk by the 15th to continue meals.")
            return redirect('dashboard')

        # Save meal
        meal, created = Meal.objects.get_or_create(student=request.user, date=meal_date)
        meal.breakfast = breakfast
        meal.lunch = lunch
        meal.dinner = dinner
        meal.save()

        messages.success(request, "Meal submitted successfully!")
        return redirect('dashboard')

    else:
        # GET request, show form with today as default
        return render(request, 'meals/meal_form.html', {'today': today})
    
    
#daily pdf:
def download_daily_meal_pdf(request):
    bd_time = datetime.now(pytz.timezone('Asia/Dhaka'))
    today = bd_time.date()

    meals = Meal.objects.filter(date=today)
    template_path = 'pdf/daily_meal_pdf.html'
    context = {'meals': meals, 'today': today}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="meal_list_{today}.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=result)

    if pisa_status.err:
        return HttpResponse('PDF generation failed')
    
    response.write(result.getvalue())
    return response


# views.py
def add_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Payment added successfully!')
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'payments/payment_form.html', {'form': form, 'title': 'Add Payment'})


def edit_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, '✏️ Payment updated successfully!')
            return redirect('payment_list')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'payments/payment_form.html', {'form': form, 'title': 'Edit Payment'})

# views.py
def payment_list(request):
    payments = Payment.objects.all().order_by('-payment_date')
    return render(request, 'payments/payment_list.html', {'payments': payments})

from django.db.models import Sum,Max

def paid_students(request):
    # Aggregate total amount paid and the latest payment date per student
    payments = Payment.objects.values('student').annotate(
        total=Sum('amount'),
        last_payment_date=Max('payment_date')
    )

    payment_details = []
    for p in payments:
        try:
            # Get the User object for the student ID
            student = User.objects.get(id=p['student'])
            
            if hasattr(student, 'studentprofile'):
                    meal_serial= student.studentprofile.meal_serial  # add meal_serial here
            else:
                    meal_serial= 9999 #default large value
                    
            payment_details.append({
                'student': student,
                'total': p['total'],
                'last_payment_date': p['last_payment_date'],
                'meal_serial': meal_serial,
                
            })
        except User.DoesNotExist:
            # Skip if the student does not exist
            continue
        
    # Sort payment_details by meal_serial ascending
    payment_details = sorted(payment_details, key=lambda x: x['meal_serial'])


    context = {'payment_details': payment_details}
    return render(request, 'payments/summary.html', context)