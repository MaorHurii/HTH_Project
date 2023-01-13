from django.urls import path
from . import views

app_name = 'university'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/home/', views.admin_home, name='admin_home'),
    path('admin/add_course/', views.add_course, name='add_course'),
    path('admin/delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('admin/edit_course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('admin/delete_report/<int:report_id>/', views.delete_report, name='delete_report'),
    path('teacher/delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/logout/', views.logout, name='logout'),
    path('teacher/home/', views.teacher_home, name='teacher_home'),
    path('teacher/upload_file/', views.upload_file, name='upload_file'),
    path('teacher/view_reports/', views.view_reports, name='view_reports'),
    path('teacher/delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('teacher/view_appointments/', views.view_appointments, name='view_appointments'),
    path('teacher/create_appointment/', views.create_appointment, name='create_appointment'),
    path('teacher/delete_appointment/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    path('teacher/view_questions/', views.view_questions, name='view_questions'),
    path('teacher/create_question/', views.create_question, name='create_question'),
    path('teacher/delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    path('teacher/answer_question/<int:question_id>/', views.answer_question, name='answer_question'),
    path('student/login/', views.student_login, name='student_login'),
    path('student/logout/', views.logout, name='logout'),
    path('student/home/', views.student_home, name='student_home'),
    path('student/view_questions/', views.view_questions, name='view_questions'),
    path('student/create_question/', views.create_question, name='create_question'),
    path('student/upload_file/', views.upload_file, name='upload_file'),
    path('student/redeem_scholarship/', views.redeem_scholarship, name='redeem_scholarship'),
]
