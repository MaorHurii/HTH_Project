from django.contrib import admin

from .models import Course, Report, Appointment, Question, Answer

admin.site.register(Course)
admin.site.register(Report)
admin.site.register(Appointment)
admin.site.register(Question)
admin.site.register(Answer)
