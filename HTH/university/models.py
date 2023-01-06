from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)


class Appointment(models.Model):
    student = models.CharField(max_length=255)
    time = models.DateTimeField()


class Report(models.Model):
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='reports/')
    uploader = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class File(models.Model):
    file = models.FileField(upload_to='files/')
    uploader = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.TextField()
