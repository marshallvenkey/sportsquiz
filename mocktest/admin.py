from django.contrib import admin
from .models import Sclass, Subject, Chapter, Slesson, Question, UserDetail, TestResult, FinalResult
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin.options import ModelAdmin

class SclassAdmin(ModelAdmin):
	

	list_display = ["name" ]
	 
	search_fields = ["name"]
	list_filter = ["name"]
admin.site.register(Sclass,SclassAdmin)

class SubjectAdmin(ModelAdmin):
	

	list_display = ["sname" ]
	 
	search_fields = ["sname"]
	list_filter = ["sname"]
admin.site.register(Subject,SubjectAdmin)


class ChapterAdmin(ModelAdmin):
	

	list_display = ["name" ]
	 
	search_fields = ["name"]
	list_filter = ["name"]
admin.site.register(Chapter,ChapterAdmin)




class SlessonAdmin(ModelAdmin):


	
	list_display = ["id","slesson"]
	 
	search_fields =["slesson"]
	list_filter = ["slesson"]

admin.site.register(Slesson,SlessonAdmin)    
# Register your models with the admin site
 
class QuestionAdmin(ImportExportModelAdmin):


	
	list_display = ["slesson","question"]
	 
	search_fields =["slesson"]
	list_filter = ["slesson"] 

admin.site.register(Question,QuestionAdmin)     

class UserDetailAdmin(ModelAdmin):
	

	list_display = ["studentname" ]
	 
	search_fields = ["studentname"]
	list_filter = ["studentname"]
admin.site.register(UserDetail,UserDetailAdmin)

 
admin.site.register(TestResult)
admin.site.register(FinalResult)
