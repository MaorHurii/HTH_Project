from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Course, Appointment, Report, Question, Answer, File
from .forms import CourseForm, AppointmentForm, AnswerForm


ADMIN_ROLE = 'Admin'
TEACHER_ROLE = 'Teacher'
STUDENT_ROLE = 'Student'
TEACHER_ADMIN_ROLE = 'student_admin'
STUDENT_TEACHER_ROLE = 'student_teacher'


def index(request):
    return render(request, 'university/index.html')


def login(request, role):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None and validate_role(user, role):
        login_user(request, user)
        return True
    else:
        messages.warning(request, 'Invalid username or password')
        return False


def validate_role(user, role):
    if role == ADMIN_ROLE:
        return user.is_superuser
    elif role == TEACHER_ADMIN_ROLE:
        return user.is_superuser or user.groups.filter(name=TEACHER_ROLE).exists()
    elif not user.is_superuser and role != STUDENT_TEACHER_ROLE:
        return user.groups.filter(name=role).exists()
    elif role == STUDENT_TEACHER_ROLE:
        return user.groups.filter(name__in=[TEACHER_ROLE, STUDENT_ROLE]).exists()
    return False


def role_required(role):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            # Check if user is authenticated
            if not request.user.is_authenticated:
                return login_required(func)(request, *args, **kwargs)
            # check if user has the required role
            if not validate_role(request.user, role):
                return HttpResponseForbidden('You do not have the required role to access this page')
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


@login_required
def logout(request):
    logout_user(request)
    return redirect('index')

# Admin context start


def admin_login(request):
    if request.method == 'POST':
        if login(request, ADMIN_ROLE):
            return redirect('admin_home')
        else:
            return redirect('admin_login')
    return render(request, 'university/admin_login.html', {'user': request.user})


@role_required(ADMIN_ROLE)
def admin_home(request):
    courses = Course.objects.all()
    teacher_files = File.objects.filter(teacher_file=True)
    student_files = File.objects.filter(teacher_file=False)
    context = {
        'courses': courses,
        'teacher_files': teacher_files,
        'student_files': student_files
    }
    return render(request, 'university/admin_home.html', context)


@role_required(ADMIN_ROLE)
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            Course.objects.create(name=name, category=category)
            return redirect('admin_home')
    else:
        form = CourseForm()
    return render(request, 'university/add_course.html', {'form': form})


@role_required(ADMIN_ROLE)
def view_courses(request):
    courses = Course.objects.all()
    return render(request, 'university/view_courses.html', {'courses': courses})


@role_required(ADMIN_ROLE)
def edit_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = CourseForm(instance=course)
    return render(request, 'university/edit_course.html', {'form': form})


@role_required(ADMIN_ROLE)
def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    return redirect('admin_home')


@role_required(ADMIN_ROLE)
def delete_report(request, report_id):
    report = Report.objects.get(id=report_id)
    report.delete()
    return redirect('admin_home')

# Admin context end

# Teacher context start


def teacher_login(request):
    if request.method == 'POST':
        if request.method == 'POST':
            if login(request, TEACHER_ROLE):
                return redirect('teacher_home')
            else:
                return redirect('teacher_login')
    return render(request, 'university/teacher_login.html')


@role_required(TEACHER_ROLE)
def teacher_home(request):
    files = File.objects.filter(teacher_file=True)
    return render(request, 'university/teacher_home.html', {'files': files})


@role_required(TEACHER_ROLE)
def view_reports(request):
    reports = Report.objects.all()
    return render(request, 'university/view_reports.html', {'reports': reports})


@role_required(STUDENT_TEACHER_ROLE)
def view_appointments(request):
    if validate_role(request.user, STUDENT_ROLE):
        appointments = Appointment.objects.filter(student=request.user.username)
    else:
        appointments = Appointment.objects.filter(teacher=request.user.username)
    return render(request, 'university/view_appointments.html', {'appointments': appointments})


@role_required(STUDENT_TEACHER_ROLE)
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            if validate_role(request.user, TEACHER_ROLE):
                teacher = request.user.username
                student = form.cleaned_data['student']
            else:
                student = request.user.username
                teacher = form.cleaned_data['teacher']

            time = form.cleaned_data['time']
            link = form.cleaned_data['zoom_link']
            Appointment.objects.create(teacher=teacher, student=student, time=time, zoom_link=link)
        return redirect('view_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'university/create_appointment.html', {'form': form})


@role_required(TEACHER_ROLE)
def delete_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    appointment.delete()
    return redirect('view_appointments')


@role_required(TEACHER_ROLE)
def view_questions(request):
    questions = Question.objects.all()
    return render(request, 'university/view_questions.html', {'questions': questions})


@role_required(TEACHER_ROLE)
def create_question(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        Question.objects.create(title=title, description=description)
        return redirect('view_questions')
    return render(request, 'university/create_question.html')


@role_required(TEACHER_ROLE)
def delete_question(question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    return redirect('view_questions')


@role_required(TEACHER_ROLE)
def answer_question(request, question_id):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            question = Question.objects.get(id=question_id)
            Answer.objects.create(question=question, answer=answer)
            return redirect('view_questions')
    else:
        form = AnswerForm()
    return render(request, 'university/answer_question.html', {'form': form})

# Teacher context end

# Student context start


def student_login(request):
    if request.method == 'POST':
        if login(request, STUDENT_ROLE):
            return redirect('student_home')
        else:
            return redirect('student_login')
    return render(request, 'university/student_login.html')


@role_required(STUDENT_ROLE)
def student_home(request):
    courses = Course.objects.all()
    files = File.objects.filter(teacher_file=False)
    return render(request, 'university/student_home.html', {'courses': courses, 'files': files})


@role_required(STUDENT_ROLE)
def view_questions(request):
    questions = Question.objects.all()
    return render(request, 'university/view_questions.html', {'questions': questions})


@role_required(STUDENT_ROLE)
def create_question(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        Question.objects.create(title=title, description=description)
        return redirect('view_questions')
    return render(request, 'university/create_question.html')

# Student context end


# All context start

@role_required(STUDENT_TEACHER_ROLE)
def upload_file(request, course_id):
    course_obj = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        file = request.FILES['file']
        filename = file.name
        teacher_file = validate_role(request.user, TEACHER_ROLE)
        File.objects.create(
            filename=filename, file=file, uploader=request.user.username, teacher_file=teacher_file, course=course_obj
        )
        return redirect('course', course_id=course_id)


@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    course_id = file.course.id
    # Check if the user is allowed to delete the file
    if request.user.is_superuser or request.user.username == request.user.username:
        file.file.delete()
        file.delete()
    return redirect('admin_home') if request.user.is_superuser else redirect('course', course_id)

# All context end
