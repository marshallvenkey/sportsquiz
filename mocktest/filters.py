import django_filters
from django import forms
from . models import Slesson

 

class SlessonFilter(django_filters.FilterSet):
   
    class Meta:
        model =Slesson
        fields = ( 'sclass', 'subject', 'chapter' )
