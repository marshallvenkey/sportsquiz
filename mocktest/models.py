from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return self.course_name

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    level = models.CharField(max_length=30, null=True)
    topic = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    topic_start = models.DateTimeField(null=True)
    topic_end= models.DateTimeField(null=True)
    test_attempts = models.IntegerField(default=1)

    def __str__(self):
        return self.topic

class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    question = models.CharField(max_length=200, null=True)
    option1 = models.CharField(max_length=30, null=True)
    option2 = models.CharField(max_length=30, null=True)
    option3 = models.CharField(max_length=30, null=True)
    option4 = models.CharField(max_length=30, null=True)
    answer = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.question

class UserDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    studentname = models.CharField(max_length=30, null=True)
    schoolname = models.CharField(max_length=30, null=True)
    mandalname = models.CharField(max_length=10, null=True)
    distname = models.CharField(max_length=100, null=True)
    
    

    def __str__(self):
        return self.user.first_name



class TestResult(models.Model):
    bhu = models.ForeignKey(UserDetail, on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    result = models.TextField(null=True)
    date1 = models.DateField(auto_now_add=True)
    marks = models.IntegerField(null=True)
    

    def __str__(self):
        return self.topic.topic+" "+self.topic.course.course_name
    def get_test_time_display(self):
        duration = self.start_time - self.end_time
        minutes = duration.total_seconds() // 60
        seconds = duration.total_seconds() % 60
        return f"{int(minutes)} minutes, {int(seconds)} seconds"    


class FinalResult(models.Model):
    quiz = models.ForeignKey(TestResult, on_delete=models.CASCADE, null=True)
    que = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    your_ans = models.CharField(max_length=100, null=True)
    def __str__(self):
        return self.que.question










