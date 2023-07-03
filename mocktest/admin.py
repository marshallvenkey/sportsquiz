from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin.options import ModelAdmin
from import_export import resources, fields
from .models import *
from import_export.fields import Field
from import_export import fields, resources, widgets
from import_export.widgets import ForeignKeyWidget
from django import forms

@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    list_display = ["question", "topic"]

    search_fields = ["question", "topic"]
    list_filter = ["question", "topic"]

    resources_class = resources.ModelResource(
        fields=[
            fields.Field(
                column_name="topic",
                attribute="topic",
                widget=ForeignKeyWidget(Topic, "topic"),
            )
        ]
    )


admin.site.register(Course)


class TopicAdmin(admin.ModelAdmin):
    list_display = ['course', 'level', 'topic', 'test_attempts']
    actions = ['reset_test_attempts']

    def reset_test_attempts(self, request, queryset):
        queryset.update(test_attempts=1)

    reset_test_attempts.short_description = "Reset test attempts"

admin.site.register(Topic, TopicAdmin)

 

@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('user', )

admin.site.register(TestResult)
admin.site.register(FinalResult)
