from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields
from .models import *

class QuestionResource(resources.ModelResource):
    course_name = fields.Field(attribute='topic__course__course_name', column_name='Course Name')
    topic_name = fields.Field(attribute='topic__topic', column_name='Topic Name')

    class Meta:
        model = Question
        fields = ('id', 'question', 'option1', 'option2', 'option3', 'option4', 'answer', 'course_name', 'topic_name')

@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    resource_class = QuestionResource
    list_display = ["question", "topic"]
    search_fields = ["question", "topic__topic"]
    list_filter = ["topic"]

@admin.register(Topic)
class TopicAdmin(ImportExportModelAdmin):
    
    list_display = ["id", "topic"]
    
admin.site.register(Course)
 
admin.site.register(UserDetail)
admin.site.register(TestResult)
admin.site.register(FinalResult)
