from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (SurveyUser, Survey, Question, ShortAnswer, ParagraphAnswer,
    DateAnswer, TimeAnswer, DateTimeAnswer, Submission)


@admin.register(SurveyUser)
class SurveyUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name']


class QuestionInline(admin.TabularInline):
    model = Question


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Submission)

admin.site.register(ShortAnswer)
admin.site.register(ParagraphAnswer)
admin.site.register(DateTimeAnswer)
admin.site.register(DateAnswer)
admin.site.register(TimeAnswer)

