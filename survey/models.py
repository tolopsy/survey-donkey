from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.exceptions import ValidationError

from .subroutines import random_id
from .fields import OrderField


class SurveyUser(AbstractUser):
    pass

    def __str__(self):
        return self.username


class Survey(models.Model):
    creator = models.ForeignKey(SurveyUser, on_delete=models.CASCADE, related_name="surveys")
    unique_id = models.CharField(max_length=50, default=random_id, unique=True)  # to be used as part of the url
    title = models.CharField(max_length=100)
    description = models.TextField()

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_updated']

    def __str__(self):
        return "%s - %s" % (self.creator.username, self.title)


class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    body = models.TextField()

    # help_label is to include hint on how to answer question (if necessary)
    help_label = models.CharField(max_length=100, blank=True, null=True)

    answer_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                    limit_choices_to={'model__contains': 'answer'})

    order = OrderField(blank=True, for_fields=['survey'])
    required = models.BooleanField(default=False)

    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return "Question %s" % self.order


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    body = models.CharField(max_length=50)

    def __str__(self):
        return self.body if(len(self.body) <= 20) else '%s...' % self.body[0:21]


class Range(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    min_value = models.PositiveIntegerField(verbose_name="minimum value")
    max_value = models.PositiveIntegerField(verbose_name="maximum value")

    def __str__(self):
        return "%s - %s" % (self.min_value, self.max_value)


class Submission(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="submissions")
    submitted_by = models.ForeignKey(SurveyUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="submissions")
    order = OrderField(blank=True, for_fields=["survey"])

    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Submission %s on %s" % (self.order, self.survey.title)


class AnswerBase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="%(class)s")
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="%(class)s")

    class Meta:
        abstract = True


class ShortAnswer(AnswerBase):
    answer = models.CharField(max_length=100)

    def __str__(self):
        return self.answer if (len(self.answer) <= 20) else "%s..." % self.answer[0:21]


class ParagraphAnswer(AnswerBase):
    answer = models.TextField()

    def __str__(self):
        return "%s..." % self.answer[0:20]


class DateAnswer(AnswerBase):
    answer = models.DateField()

    def __str__(self):
        return self.answer


class TimeAnswer(AnswerBase):
    answer = models.TimeField(default=timezone.now)

    def __str__(self):
        return self.answer


class DateTimeAnswer(AnswerBase):
    answer = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.answer


class SelectOneAnswer(AnswerBase):
    answer = models.ForeignKey(Option, on_delete=models.PROTECT)

    def __str__(self):
        return '%s' % self.answer.body if(len(self.answer.body) <= 20) else '%s...' % self.answer.body[0:21]


class SelectMultipleAnswer(AnswerBase):
    answer = models.ManyToManyField(Option)

    def __str__(self):
        display_text = ""
        for each in self.answer.all():
            if each == self.answer.all()[0]:
                display_text += "%s " % each
                continue
            display_text += "| %s " % each

        return display_text


class RangeAnswer(AnswerBase):
    range_obj = models.ForeignKey(Range, on_delete=models.PROTECT)
    answer = models.PositiveIntegerField()

    def clean(self):
        try:
            if (self.answer >= self.range_obj.min_value) and (self.answer <= self.range_obj.max_value):
                super(RangeAnswer, self).clean()
            else:
                raise ValidationError("Answer is not within range of %s - %s" %
                                      (self.range_obj.min_value, self.range_obj.max_value))

        except ValidationError:
            raise ValidationError(
                "Answer is not within range of %s - %s" % (self.range_obj.min_value, self.range_obj.max_value))
        '''
        except:
            super(RangeAnswer, self).clean()
        '''

    def __str__(self):
        return "%s within %s" % (self.answer, self.range_obj)
