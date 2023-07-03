from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import UserSchedule

class DashboardAccessScheduleForm(forms.ModelForm):
    class Meta:
        model = UserSchedule
        fields = ['dashboard_access_schedule_start', 'dashboard_access_schedule_end']
        widgets = {
            'dashboard_access_schedule_start': forms.DateTimeInput(attrs={'class': 'datetimepicker'}),
            'dashboard_access_schedule_end': forms.DateTimeInput(attrs={'class': 'datetimepicker'}),
        }
class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2']
