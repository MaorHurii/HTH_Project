from django import forms
from .models import Course, Appointment, Question, Answer, Report, File


class CourseForm(forms.Form):
    name = forms.CharField(max_length=255)
    category = forms.CharField(max_length=255)


class AppointmentForm(forms.Form):
    student = forms.CharField(max_length=255)
    time = forms.DateTimeField()


class AnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea)


class FileForm(forms.Form):
    file = forms.FileField()


class QuestionForm(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255, widget=forms.Textarea)
