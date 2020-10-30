from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import SurveyUser, Survey


@admin.register(SurveyUser)
class SurveyUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name']


admin.site.register(Survey)

