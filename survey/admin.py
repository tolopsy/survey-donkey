from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import SurveyUser, Survey, Question


@admin.register(SurveyUser)
class SurveyUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name']


class QuestionInline(admin.TabularInline):
    model = Question


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

