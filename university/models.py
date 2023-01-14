from django.db import models


class Course(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)


class File(models.Model):
    objects = models.Manager()
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    uploader = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    teacher_file = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='files')


class Question(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=255)
    body = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    creator = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class Answer(models.Model):
    objects = models.Manager()
    creator = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Appointment(models.Model):
    objects = models.Manager()
    time = models.DateField()
    teacher = models.CharField(max_length=255)
    student = models.CharField(max_length=255)
    zoom_link = models.CharField(max_length=255)


class Scholarship(models.Model):
    objects = models.Manager()
    student = models.CharField(max_length=255)


class Meta:
    app_label = 'university'
