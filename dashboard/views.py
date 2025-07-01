from django.shortcuts import render
from symptom_checker.models import UserSymptom, Disease
from django.shortcuts import get_object_or_404, render
from symptom_checker.models import UserSymptom

from django.shortcuts import render
from django.db.models import Count, Q
from django.http import JsonResponse
from patients.models import Patient 
import json

def dashboard(request):
    patients = Patient.objects.all()
    gender_counts = patients.values('gender').annotate(count=Count('id'))
    genders = [item['gender'] for item in gender_counts]
    gender_values = [item['count'] for item in gender_counts]

    status_counts = patients.values('status').annotate(count=Count('id'))
    statuses = [item['status'] for item in status_counts]
    status_values = [item['count'] for item in status_counts]

    symptoms = UserSymptom.objects.all()
    disease_counts = symptoms.values('disease__name').annotate(count=Count('id')).order_by('-count')
    diseases = [item['disease__name'] or 'Unknown' for item in disease_counts]
    disease_values = [item['count'] for item in disease_counts]

    context = {
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

def admin_dashboard(request):
    total_patients = Patient.objects.count()

    # Gender distribution
    gender_data = Patient.objects.values('gender').annotate(count=Count('gender'))

    # Diagnosis count per disease
    disease_data = (
        UserSymptom.objects.values('disease__name')
        .annotate(count=Count('disease'))
        .order_by('-count')
    )

    # Monthly patients for last 6 months
    six_months_ago = now() - timedelta(days=180)

    patients_by_month = (
        Patient.objects.filter(created_at__gte=six_months_ago)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )


    monthly_data = [
        {'month': item['month'].strftime('%Y-%m'), 'count': item['count']}
        for item in patients_by_month
    ]

    context = {
        'total_patients': total_patients,
        'gender_data': list(gender_data),
        'disease_data': list(disease_data),
        'patients_by_month': monthly_data,
    }

    return render(request, 'pages/admin_dashboard.html', context)


def manage_users(request):
    return render(request, 'pages/manage_users.html')