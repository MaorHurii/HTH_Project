from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.forms import SelectDateWidget

from .constants import USER_ROLES, STUDENT_ROLE
from .models import Course, Appointment, Question, Answer, File




def get_student_list():
    student_group = Group.objects.get(name=STUDENT_ROLE)
    students = student_group.user_set.all()
    # This returns the students list in the required format for the choices field [(s1,s1),(s2,s2)..]
    return [(student.username, student.username) for student in students]

def get_teacher_list():
    teacher_group = Group.objects.get(name=STUDENT_ROLE)
    teachers = teacher_group.user_set.all()
    # This returns the students list in the required format for the choices field [(s1,s1),(s2,s2)..]
    return [(teacher.username, teacher.username) for teacher in teachers]


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'category']


class AppointmentForm(forms.ModelForm):
    time = forms.DateField(widget=SelectDateWidget)
    student = forms.ChoiceField(choices=get_student_list, label='student', required=False)
    teacher = forms.ChoiceField(choices=get_teacher_list, label='teacher', required=False)



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body']



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
