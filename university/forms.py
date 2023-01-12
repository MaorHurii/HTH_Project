from django import forms
from .models import Course, Appointment, Question, Answer, Report, File

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'category']



class AppointmentForm(forms.ModelForm):
    time = forms.DateField(widget=SelectDateWidget)
    student = forms.ChoiceField(choices=get_student_list, label='student', required=False)
    teacher = forms.ChoiceField(choices=get_teacher_list, label='teacher', required=False)

    class Meta:
        model = Appointment
        fields = ['zoom_link']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'description']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question', 'answer']


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['filename', 'file', 'uploader']


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['filename', 'file', 'uploader']
