from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (SurveyUser, Survey, Question, Option, Range, ShortAnswer, ParagraphAnswer,
                     DateAnswer, TimeAnswer, DateTimeAnswer, SelectOneAnswer, SelectMultipleAnswer,
                     RangeAnswer, Submission)


def view_inline(obj=None):
    if obj.pk:
        url = reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk])
        return mark_safe('<a href="{}">View / Change </a>'.format(url))
    else:
        return "Save, then click here to go to %s" % obj._meta.model_name


view_inline.short_description = "View Inline"


class QuestionInline(admin.StackedInline):
    model = Question
    fields = ['body', 'help_label', 'answer_type', 'required', view_inline, ]
    readonly_fields = [view_inline, ]
    extra = 0


class OptionInline(admin.TabularInline):
    model = Option
    extra = 0


class RangeInline(admin.TabularInline):
    model = Range
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline, RangeInline]


@admin.register(SurveyUser)
class SurveyUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'first_name', 'last_name']


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Submission)

admin.site.register(ShortAnswer)
admin.site.register(ParagraphAnswer)
admin.site.register(DateTimeAnswer)
admin.site.register(DateAnswer)
admin.site.register(TimeAnswer)
admin.site.register(SelectOneAnswer)
admin.site.register(SelectMultipleAnswer)
admin.site.register(RangeAnswer)

