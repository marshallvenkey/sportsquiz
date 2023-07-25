from django.urls import path
from . import views
app_name = 'mocktest'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),  # Updated URL pattern
    path('user-details/<int:user_id>/', views.user_details, name='user_details'),
    path('logout/', views.user_logout, name='user_logout'),  # Updated URL pattern
    path('dashboard/', views.dashboard, name='dashboard'),
    path('test/<int:slesson_id>/', views.take_test, name='take_test'),
    path('result/<int:result_id>/', views.result, name='result'),
    path('previous-results/', views.previous_results, name='previous_results'),
    
     
    path('user-profile/', views.user_profile, name='user_profile'),
    path('test_attempts_exceeded/', views.test_attempts_exceeded, name='test_attempts_exceeded'),

]
