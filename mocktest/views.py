from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.paginator import Paginator
from datetime import datetime 
import json
 
from django.http import JsonResponse
 
from .models import TestResult
from django.utils import timezone

from django.http import JsonResponse

@login_required
def previous_results(request):
    course_id = request.GET.get('course_id')
    topic_id = request.GET.get('topic_id')

    test_results = TestResult.objects.filter(bhu__user=request.user)

    if course_id:
        test_results = test_results.filter(topic__course_id=course_id)
    if topic_id:
        test_results = test_results.filter(topic_id=topic_id)

    # Pagination
    paginator = Paginator(test_results, 10)  # Display 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'courses': Course.objects.all(),
        'topics': Topic.objects.filter(course_id=course_id) if course_id else Topic.objects.none()
    }

    return render(request, 'mocktest/previous_results.html', context)


 

@login_required
def get_topics(request):
    course_id = request.GET.get('course_id')
    if course_id:
        topics = Topic.objects.filter(course_id=course_id)
    else:
        topics = Topic.objects.all()
    options = '<option value="">All</option>'
    for topic in topics:
        options += f'<option value="{topic.id}">{topic.topic}</option>'
    return JsonResponse(options, safe=False)
 

@login_required
def take_test(request, topic_id):
    topic = Topic.objects.get(pk=topic_id)
    current_time = timezone.now()
    questions = topic.question_set.all()
    user = request.user
    question_count = len(questions)

    if current_time < topic.topic_start or current_time > topic.topic_end:
        return render(request, 'mocktest/topic_not_started.html', {'topic': topic})

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

            score = calculate_score(topic, user_answers)

            result_json = json.dumps(user_answers)
            user_details = UserDetail.objects.filter(user=user)
            if user_details.exists():
                user_detail = user_details.first()
            else:
                user_detail = UserDetail.objects.create(user=user)

            test_results = TestResult.objects.filter(bhu=user_detail, topic=topic)

            if test_results.count() >= topic.test_attempts:
                return render(request, 'mocktest/test_attempts_exceeded.html', {'topic': topic})

            test_result = TestResult.objects.create(
                bhu=user_detail,
                topic=topic,
                result=result_json,
                marks=score,
                date1=timezone.now(),
            )

            return redirect('result', result_id=test_result.id)

        # Redirect to the next question
        next_question_index = question_index + 1
        next_question = questions[next_question_index]
        context = {
            'topic': topic,
            'question': next_question,
            'question_index': next_question_index,
            'question_count': question_count,
            'current_time': current_time,
        }
        return render(request, 'mocktest/take_test.html', context)

    # Initial request or GET request for the first question
    context = {
        'topic': topic,
        'question': questions[0],
        'question_index': 0,
        'question_count': question_count,
        'current_time': current_time,
    }

    # Check if the user has already exceeded the test attempts
    user_details = UserDetail.objects.filter(user=user)
    if user_details.exists():
        user_detail = user_details.first()
        test_results = TestResult.objects.filter(bhu=user_detail, topic=topic)
        if test_results.count() >= topic.test_attempts:
            return render(request, 'mocktest/test_attempts_exceeded.html', {'topic': topic})

    return render(request, 'mocktest/take_test.html', context)


def test_attempts_exceeded(request):
    return render(request, 'mocktest/test_attempts_exceeded.html')


@login_required
def result(request, result_id):
    try:
        test_result = get_object_or_404(TestResult, pk=result_id)
        questions = Question.objects.filter(topic=test_result.topic)
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

def calculate_score(topic, user_answers):
    # Perform the score calculation logic here
    # You can access the correct answers for each question through the topic object
    # Compare the user's answers with the correct answers and calculate the score
    # Return the calculated score

    # Example implementation (replace with your own logic):
    score = 0
    questions = topic.question_set.all()
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
            return redirect('user_details', user_id=user.id)
    else:
        form = UserCreationForm()
    return render(request, 'mocktest/register.html', {'form': form})

def user_details(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        studentname = request.POST.get('studentname')
        schoolname = request.POST.get('schoolname')
        mandalname = request.POST.get('mandalname')
        distname = request.POST.get('distname')

        UserDetail.objects.create(user=user, studentname=studentname, schoolname=schoolname, mandalname=mandalname, distname=distname)
        return redirect('user_login')

    return render(request, 'mocktest/user_details.html', {'user': user})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'mocktest/login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'mocktest/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    courses = Course.objects.all()
    topics = Topic.objects.all()
    
    # Get the UserSchedule for the current user
     
    
    context = {
        'courses': courses,
        'topics': topics,
         
    }
    
    return render(request, 'mocktest/dashboard.html', context)
    
@login_required
def user_profile(request):
    user = request.user
    user_detail = UserDetail.objects.get(user=user)
    context = {'user_detail': user_detail}
    return render(request, 'mocktest/user_profile.html', context)