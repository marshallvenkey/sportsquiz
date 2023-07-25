from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class Sclass(models.Model):
    CLASS_CHOICES = ( 
        ("-SELECT-", "-SELECT-"),       
        ("10 EM", "10 EM"), 
        ("10 TM", "10 TM"), 
        ("9 EM", "9 EM"), 
        ("9 TM", "9 TM"),
        ("8 EM", "8 EM"), 
        ("8 TM", "8 TM"),
        ("7 EM", "7 EM"), 
        ("7 TM", "7 TM"),
        ("6 EM", "6 EM"), 
        ("6 TM", "6 TM"), 
    ) 

    name = models.CharField(max_length=40, choices=CLASS_CHOICES, default=None)

    def __str__(self):
        return self.name

class Subject(models.Model):
    SUB_CHOICES = ( 
        ("-SELECT-", "-SELECT-"),     
        ("TELUGU", "TELUGU"), 
        ("HINDI", "HINDI"), 
        ("ENGLISH", "ENGLISH"), 
        ("MATHS", "MATHS"), 
        ("PHYSCI", "PHYSCI"),
        ("BIOSCI", "BIOSCI"),
        ("SOCIAL", "SOCIAL"),   
    ) 
    sclass = models.ForeignKey(Sclass, on_delete=models.CASCADE, default=None)
    sname = models.CharField(max_length=40, choices=SUB_CHOICES, default='TELUGU')

    def __str__(self):
        return self.sname

class Chapter(models.Model):
    CHAPTER_CHOICES = ( 
        ("-SELECT-", "-SELECT-"),       
        ("chapter 1", "chapter 1"), 
        ("chapter 2", "chapter 2"), 
        ("chapter 3", "chapter 3"), 
        ("chapter 4", "chapter 4"), 
    )
    sclass = models.ForeignKey(Sclass, on_delete=models.CASCADE, default=None, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=None, null=True)
    name = models.CharField(max_length=40, choices=CHAPTER_CHOICES)

    def __str__(self):
        return self.name

class Slesson(models.Model):
    slesson = models.CharField(max_length=124)
    sclass = models.ForeignKey(Sclass, on_delete=models.CASCADE, default=None)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, default=None)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.slesson

   

class Question(models.Model):
    slesson = models.ForeignKey(Slesson, on_delete=models.CASCADE, null=True)
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
    slesson = models.ForeignKey(Slesson, on_delete=models.CASCADE, null=True)
    result = models.TextField(null=True)
    date1 = models.DateField(auto_now_add=True)
    marks = models.IntegerField(null=True)
    

    def __str__(self):
        return self.slesson.slesson+" "+self.slesson.subject.sname
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










