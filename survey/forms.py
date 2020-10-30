from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import SurveyUser


class SurveyUserCreationForm(UserCreationForm):
    class Meta:
        model = SurveyUser
        fields = ['username', 'email']


class SurveyUserChangeForm(UserChangeForm):
    class Meta:
        model = SurveyUser
        fields = ['username', 'email']

