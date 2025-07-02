from django.shortcuts import render
from symptom_checker.models import UserSymptom, Disease
from django.shortcuts import get_object_or_404, render
from symptom_checker.models import UserSymptom
from django.contrib.auth import get_user_model

from django.shortcuts import render
from django.db.models import Count
import json

from patients.models import Patient
from symptom_checker.models import UserSymptom
def dashboard(request):
    patients = Patient.objects.all()

    # Gender breakdown
    gender_counts = patients.values('gender').annotate(count=Count('id'))
    genders = [item['gender'] or 'Unknown' for item in gender_counts]
    gender_values = [item['count'] for item in gender_counts]

    # Status breakdown
    status_counts = patients.values('status').annotate(count=Count('id'))
    statuses = [item['status'] or 'Unknown' for item in status_counts]
    status_values = [item['count'] for item in status_counts]

    # Disease frequency from UserSymptom records
    symptoms = UserSymptom.objects.all()
    disease_counts = symptoms.values('disease__name').annotate(count=Count('id')).order_by('-count')
    diseases = [item['disease__name'] or 'Unknown' for item in disease_counts]
    disease_values = [item['count'] for item in disease_counts]

    # Top metrics for cards
    total_patients = patients.count()
  
    male_patients = patients.filter(gender='Male').count()
    female_patients = patients.filter(gender='Female').count()

    context = {
        'total_patients': total_patients,
       
        'male_patients': male_patients,
        'female_patients': female_patients,

        'genders': json.dumps(genders),
        'gender_values': json.dumps(gender_values),

        'statuses': json.dumps(statuses),
        'status_values': json.dumps(status_values),

        'diseases': json.dumps(diseases),
        'disease_values': json.dumps(disease_values),
    }

    return render(request, 'dashboard/dashboard.html', context)


def diagnostics(request):
    return render(request, 'pages/diagnostics.html')

# from patients.models import Patient  # import Patient model



def users(request):
    return render(request, 'pages/users.html')


from django.core.paginator import Paginator
from django.shortcuts import render


def medical_records(request):
    record_list = UserSymptom.objects.all().order_by('-created_at')
    paginator = Paginator(record_list, 10)

    page_number = request.GET.get('page')
    records = paginator.get_page(page_number)

    return render(request, 'pages/medical_records.html', {'records': records})


def symptom_checker(request):
    return render(request, 'pages/symptom_checker.html')

from symptom_checker.models import UserSymptom

from django.shortcuts import render, redirect, get_object_or_404
from symptom_checker.models import UserSymptom
from django.db.models import Q

def test_results(request):
    query = request.GET.get('q', '')
    if query:
        test_results = UserSymptom.objects.filter(
            Q(disease__name__icontains=query) |
            Q(symptoms__icontains=query) |
            Q(user_id__icontains=query)
        ).order_by('-created_at')
    else:
        test_results = UserSymptom.objects.all().order_by('-created_at')

    return render(request, 'pages/test_results.html', {
        'test_results': test_results,
        'query': query
    })

def delete_test_result(request, pk):
    result = get_object_or_404(UserSymptom, pk=pk)
    result.delete()
    return redirect('test_results') 


def recommendations(request):
    return render(request, 'pages/recommendations.html')

def reports(request):
    return render(request, 'pages/reports.html')

def notifications(request):
    return render(request, 'pages/notifications.html')

def system_settings(request):
    return render(request, 'pages/system_settings.html')

def admin_users(request):
    return render(request, 'pages/admin_users.html')

def logout_view(request):
    return render(request, 'pages/logout.html')

def record_detail(request, pk):
    record = get_object_or_404(UserSymptom, pk=pk)
    return render(request, 'pages/record_detail.html', {'record': record})

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def record_delete(request, id):
    if request.method == 'POST':
        record = get_object_or_404(UserSymptom, id=id)
        record.delete()
        messages.success(request, "Medical record deleted successfully.")
    return redirect('medical_records')


from django.shortcuts import render
from django.db.models import Count
from django.utils.timezone import now
from datetime import timedelta
from django.db.models.functions import TruncMonth
from patients.models import Patient

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from accounts.models import Account
from patients.models import Patient
from symptom_checker.models import UserSymptom

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
def admin_dashboard(request):
    # Cards Data
    total_patients = Patient.objects.count()
    active_users = Account.objects.filter(is_active=True).count()
    admins = Account.objects.filter(role='admin').count()
    doctors = Account.objects.filter(role='doctor').count()

    # Chart Data
    gender_counts = Patient.objects.values('gender').annotate(count=Count('id'))
    genders = [item['gender'] for item in gender_counts]
    gender_values = [item['count'] for item in gender_counts]

    status_counts = Patient.objects.values('status').annotate(count=Count('id'))
    statuses = [item['status'] for item in status_counts]
    status_values = [item['count'] for item in status_counts]

    disease_counts = UserSymptom.objects.values('disease__name').annotate(count=Count('id')).order_by('-count')
    diseases = [item['disease__name'] or 'Unknown' for item in disease_counts]
    disease_values = [item['count'] for item in disease_counts]

    context = {
        'total_patients': total_patients,
        'active_users': active_users,
        'admins': admins,
        'doctors': doctors,
        'genders': json.dumps(genders),
        'gender_values': json.dumps(gender_values),
        'statuses': json.dumps(statuses),
        'status_values': json.dumps(status_values),
        'diseases': json.dumps(diseases),
        'disease_values': json.dumps(disease_values),
    }

    return render(request, 'pages/admin_dashboard.html', context)


def manage_users(request):
    User = get_user_model()
    users = User.objects.all().order_by('id')
    
    context = {
        'users': users,
    }
    return render(request, 'pages/manage_users.html', context)



User = get_user_model()

from django.contrib import messages
# ... rest of imports

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.role = request.POST.get('role', user.role)
        user.is_active = bool(request.POST.get('is_active'))
        user.save()
        messages.success(request, 'User updated successfully.')
        return redirect('manage_users')

    return render(request, 'pages/edit_user.html', {'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('manage_users')
    return render(request, 'pages/delete_user_confirm.html', {'user': user})