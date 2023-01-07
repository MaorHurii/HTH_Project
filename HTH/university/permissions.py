from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from modul.university.models import Answer, Question, Appointment, Report, Course, File


# Create permission to add courses
view_courses_permission = Permission.objects.create(
    codename='add_courses',
    name='Can add courses',
    content_type=ContentType.objects.get_for_model(Course)
)

# Create permission to add courses
add_courses_permission = Permission.objects.create(
    codename='add_courses',
    name='Can add courses',
    content_type=ContentType.objects.get_for_model(Course)
)

# Create permission to edit courses
edit_courses_permission = Permission.objects.create(
    codename='edit_courses',
    name='Can edit courses',
    content_type=ContentType.objects.get_for_model(Course)
)

# Create permission to delete courses
delete_courses_permission = Permission.objects.create(
    codename='delete_courses',
    name='Can delete courses',
    content_type=ContentType.objects.get_for_model(Course)
)

# Create permission to upload files
upload_files_permission = Permission.objects.create(
    codename='upload_files',
    name='Can upload files',
    content_type=ContentType.objects.get_for_model(File)
)

# Create permission to delete files
delete_files_permission = Permission.objects.create(
    codename='delete_files',
    name='Can delete files',
    content_type=ContentType.objects.get_for_model(File)
)

# Create permission to view reports
view_reports_permission = Permission.objects.create(
    codename='view_reports',
    name='Can view reports',
    content_type=ContentType.objects.get_for_model(Report)
)

# Create permission to create appointments
create_appointments_permission = Permission.objects.create(
    codename='create_appointments',
    name='Can create appointments',
    content_type=ContentType.objects.get_for_model(Appointment)
)

# Create permission to post questions
post_questions_permission = Permission.objects.create(
    codename='post_questions',
    name='Can post questions',
    content_type=ContentType.objects.get_for_model(Question)
)

# Create permission to answer questions
answer_questions_permission = Permission.objects.create(
    codename='answer_questions',
    name='Can answer questions',
    content_type=ContentType.objects.get_for_model(Answer)
)