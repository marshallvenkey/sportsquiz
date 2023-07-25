from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.paginator import Paginator
from datetime import datetime
import json
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from django.shortcuts import render
from .filters import SlessonFilter
from .models import Slesson, Question
from mocktest.templatetags import extras

@login_required
def dashboard(request):
    context={}
    postall = SlessonFilter(request.GET, queryset=Slesson.objects.all())

    context['postall']= postall

    paginator = Paginator (postall.qs,10)
    page_number = request.GET.get('page')
    postall_paginator = paginator.get_page(page_number) 

    context['postall_paginator']= postall_paginator

    return render(request, 'mocktest/dashboard.html', context)

@login_required
def previous_results(request):
    selected_class_id = request.GET.get('sclass_id')
    selected_subject_id = request.GET.get('subject_id')

    test_results = TestResult.objects.filter(bhu__user=request.user)

    if selected_class_id:
        test_results = test_results.filter(slesson__sclass_id=selected_class_id)
    if selected_subject_id:
        test_results = test_results.filter(slesson__subject_id=selected_subject_id)

    # Pagination
    paginator = Paginator(test_results, 10)  # Display 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'sclasses': Sclass.objects.all(),
        'selected_class': int(selected_class_id) if selected_class_id else None,
        'subjects': Subject.objects.filter(sclass_id=selected_class_id) if selected_class_id else Subject.objects.none(),
        'selected_subject': int(selected_subject_id) if selected_subject_id else None,
        'current_time': timezone.now(),  # Add current_time to the context
    }

    return render(request, 'mocktest/previous_results.html', context)


 


@login_required
def take_test(request, slesson_id):
    slesson = get_object_or_404(Slesson, pk=slesson_id)
    current_time = timezone.now()
    questions = slesson.question_set.all()
    user = request.user
    question_count = len(questions)

    # Check if the user has filled in the required details
    user_details = UserDetail.objects.filter(user=user)
    if not user_details.exists():
        return redirect('mocktest:user_details', user_id=user.id)

     

    if request.method == 'POST':
        question_index = int(request.POST.get('question_index', 0))
        question_id = request.POST.get('question_id')

        # Get the user's answer for the current question
        user_answer = request.POST.get('question_' + question_id)

        # Save the user's answer in session or database, depending on your requirements
        request.session['question_' + question_id] = user_answer

        # Check if it is the last question
        if question_index + 1 >= question_count:
            # All questions answered, calculate score and redirect to result page
            user_answers = {}
            for question in questions:
                question_id = str(question.id)
                user_answers[question_id] = request.session.get('question_' + question_id)

            score = calculate_score(slesson, user_answers)

            result_json = json.dumps(user_answers)
            user_details = UserDetail.objects.filter(user=user)
            if user_details.exists():
                user_detail = user_details.first()
            else:
                user_detail = UserDetail.objects.create(user=user)

            test_results = TestResult.objects.filter(bhu=user_detail, slesson=slesson)

             

            test_result = TestResult.objects.create(
                bhu=user_detail,
                slesson=slesson,
                result=result_json,
                marks=score,
                date1=timezone.now(),
            )

            return redirect('mocktest:result', result_id=test_result.id)

        # Redirect to the next question
        next_question_index = question_index + 1
        next_question = questions[next_question_index]
        context = {
            'slesson': slesson,
            'question': next_question,
            'question_index': next_question_index,
            'question_count': question_count,
            'current_time': current_time,
        }
        return render(request, 'mocktest/take_test.html', context)

    # Initial request or GET request for the first question
    context = {
        'slesson': slesson,
        'question': questions[0],
        'question_index': 0,
        'question_count': question_count,
        'current_time': current_time,
    }

    # Check if the user has already exceeded the test attempts
    user_details = UserDetail.objects.filter(user=user)
    if user_details.exists():
        user_detail = user_details.first()
        test_results = TestResult.objects.filter(bhu=user_detail, slesson=slesson)
        

    return render(request, 'mocktest/take_test.html', context)


def test_attempts_exceeded(request):
    return render(request, 'mocktest/test_attempts_exceeded.html')

@login_required
def result(request, result_id):
    try:
        test_result = get_object_or_404(TestResult, pk=result_id)
        slesson = test_result.slesson

        

        questions = Question.objects.filter(slesson=slesson)
        user_answers = json.loads(test_result.result)  # Convert the JSON string to a Python dictionary
        
        # Get the user's selected answers for each question
        question_answers = []
        for question in questions:
            question_id = str(question.id)
            user_answer = user_answers.get(question_id)
            question_answers.append((question, user_answer))
        
        return render(request, 'mocktest/result.html', {'test_result': test_result, 'question_answers': question_answers})
    except TestResult.DoesNotExist:
        return render(request, 'mocktest/empty_result.html')


def calculate_score(slesson, user_answers):
    # Perform the score calculation logic here
    # You can access the correct answers for each question through the slesson object
    # Compare the user's answers with the correct answers and calculate the score
    # Return the calculated score

    # Example implementation (replace with your own logic):
    score = 0
    questions = slesson.question_set.all()
    for question in questions:
        question_id = str(question.id)
        correct_answer = question.answer
        user_answer = user_answers.get(question_id)
        if user_answer == correct_answer:
            score += 1

    return score


def home(request):
    return render(request, 'mocktest/home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('mocktest:user_details', user_id=user.id)
    else:
        form = UserCreationForm()
    return render(request, 'mocktest/register.html', {'form': form})

@login_required
def user_details(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        studentname = request.POST.get('studentname')
        schoolname = request.POST.get('schoolname')
        mandalname = request.POST.get('mandalname')
        distname = request.POST.get('distname')

        # Check if a UserDetail object already exists for the user
        user_detail, created = UserDetail.objects.get_or_create(user=user)

        # Update the user details
        user_detail.studentname = studentname
        user_detail.schoolname = schoolname
        user_detail.mandalname = mandalname
        user_detail.distname = distname
        user_detail.save()

        return redirect('mocktest:dashboard')

    return render(request, 'mocktest/user_details.html', {'user': user})



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mocktest:home')
        else:
            return render(request, 'mocktest/login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'mocktest/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('mocktest:user_login')


    
@login_required
def user_profile(request):
    user = request.user

    try:
        user_detail = UserDetail.objects.get(user=user)
    except UserDetail.DoesNotExist:
        # UserDetail object does not exist, redirect to user_details view
        return redirect('mocktest:user_details', user_id=user.id)

    context = {'user_detail': user_detail}
    return render(request, 'mocktest/user_profile.html', context)