# teachers/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.teacher_login, name='teacher_login'),
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('results/', views.view_student_results, name='view_student_results'),
   
    
]
