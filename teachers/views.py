# teachers/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mocktest.models import *
 

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
import io
import csv

def bulk_register_users(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a CSV file.')
            return redirect('mocktest:bulk_register')

        try:
            # Assuming the CSV file has a 'username' column
            # Open the CSV file in text mode using io.TextIOWrapper
            csv_file_text = io.TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.DictReader(csv_file_text)
            common_password = 'Qwerty@123'
            for row in reader:
                username = row.get('username')
                if not User.objects.filter(username=username).exists():
                    # Create a user with the common password
                    user = User.objects.create_user(username=username, password=common_password)
                    # Add any additional logic to set other user attributes as needed
                    user.save()
            messages.success(request, 'Users registered successfully.')
        except Exception as e:
            messages.error(request, f'Error while registering users: {str(e)}')
        return redirect('teachers:bulk_register')

    return render(request, 'bulk_register.html')

 

@login_required
def view_student_results(request):
    slesson_id = request.GET.get('slesson_id')
    subject_id = request.GET.get('subject_id')
    sclass_id = request.GET.get('sclass_id')
    sort_by = request.GET.get('sort_by', 'marks')  # Default sort by marks

    test_results = TestResult.objects.all()  # Get all test results

    if slesson_id:
        test_results = test_results.filter(slesson_id=slesson_id)

    if subject_id:
        test_results = test_results.filter(slesson__subject_id=subject_id)

    if sclass_id:
        test_results = test_results.filter(slesson__sclass_id=sclass_id)

    if sort_by == 'marks':
        test_results = test_results.order_by('-marks')  # Sort by descending marks

    context = {
        'test_results': test_results,
        'slessons': Slesson.objects.all(),
        'subjects': Subject.objects.all(),
        'sclasses': Sclass.objects.all(),
        'selected_slesson': int(slesson_id) if slesson_id else None,
        'selected_subject': int(subject_id) if subject_id else None,
        'selected_sclass': int(sclass_id) if sclass_id else None,
        'sort_by': sort_by
    }

    return render(request, 'view_student_results.html', context)



from django.contrib.auth.models import User

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and (hasattr(user, 'teacher') or user.is_superuser):
            login(request, user)
            return redirect('teachers:teacher_dashboard')
        else:
            error_message = "Invalid username or password."
    else:
        error_message = ""
    return render(request, 'teacher_login.html', {'error_message': error_message})

@login_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')