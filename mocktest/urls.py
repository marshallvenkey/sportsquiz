from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),  # Updated URL pattern
    path('user-details/<int:user_id>/', views.user_details, name='user_details'),
    path('logout/', views.user_logout, name='user_logout'),  # Updated URL pattern
    path('dashboard/', views.dashboard, name='dashboard'),
    path('test/<int:topic_id>/', views.take_test, name='take_test'),
    path('result/<int:result_id>/', views.result, name='result'),
    path('previous-results/', views.previous_results, name='previous_results'),
    path('get-topics/', views.get_topics, name='get_topics'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('test_attempts_exceeded/', views.test_attempts_exceeded, name='test_attempts_exceeded'),

]
