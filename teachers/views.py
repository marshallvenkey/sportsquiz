# teachers/views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mocktest.models import *
 
 

@login_required
def view_student_results(request):
    topic_id = request.GET.get('topic_id')
    sort_by = request.GET.get('sort_by', 'marks')  # Default sort by marks
    test_results = TestResult.objects.all()  # Get all test results

    if topic_id:
        test_results = test_results.filter(topic_id=topic_id)

    if sort_by == 'marks':
        test_results = test_results.order_by('-marks')  # Sort by descending marks

    context = {
        'test_results': test_results,
        'topics': Topic.objects.all(),
        'selected_topic': int(topic_id) if topic_id else None,
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
            return redirect('teacher_dashboard')
        else:
            error_message = "Invalid username or password."
    else:
        error_message = ""
    return render(request, 'teacher_login.html', {'error_message': error_message})

@login_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')