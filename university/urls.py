from django.urls import path
from . import views 

app_name = 'university'

urlpatterns = [
    # General URLS
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('course/<int:course_id>', views.course, name='course'),
    path('delete_file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('upload_file/<int:course_id>/', views.upload_file, name='upload_file'),
    path('questions/<int:question_id>/', views.view_question, name='view_question'),
    path('create_question/<int:course_id>/', views.create_question, name='create_question'),
    path('delete_question/<int:question_id>/', views.delete_question, name='delete_question'),
    # Admin URLs
    path('admin/home/', views.admin_home, name='admin_home'),
    path('admin/home/<int:user_id>/delete/', views.delete_user, name='delete_user'),   
    path('admin/add_course/', views.add_course, name='add_course'),
    path('admin/edit_course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('admin/delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
    # Teacher URLs
    path('teacher/view_appointments/', views.view_appointments, name='view_appointments'),
    path('teacher/create_appointment/', views.create_appointment, name='create_appointment'),
    path('teacher/answer_question/<int:question_id>/', views.answer_question, name='answer_question'),
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
]
