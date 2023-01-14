from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect

from .constants import ADMIN_ROLE, TEACHER_ADMIN_ROLE, STUDENT_TEACHER_ROLE, TEACHER_ROLE, STUDENT_ROLE
from .models import Course, Appointment, Question, File, Answer, Scholarship
from .forms import CourseForm, AppointmentForm, AnswerForm, SignUpForm


def validate_role(user, role):
    """The function receives a user object and a role and returns True if the user is part of that group/role"""
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
    """This decorator wraps the relevant functions and manages the role requirement / permission logic"""
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


# Admin context start

@role_required(ADMIN_ROLE)
def admin_home(request):
    courses = Course.objects.all()
    users = User.objects.all()
    teacher_files = File.objects.filter(teacher_file=True)
    student_files = File.objects.filter(teacher_file=False)
    context = {
        'users' : users,
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
    """Handles the admin edit page"""
    course_obj = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course_obj)
        if form.is_valid():
            form.save()
            return redirect('admin_home')
    else:
        form = CourseForm(instance=course_obj)
    return render(request, 'university/edit_course.html', {'form': form})


@role_required(ADMIN_ROLE)
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('admin_home')

@role_required(ADMIN_ROLE)
def delete_course(request, course_id):
    course_obj = Course.objects.get(id=course_id)
    course_obj.delete()
    return redirect('admin_home')


# Admin context end

# Teacher context start

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

# Teacher context end

# Student context start

@role_required(STUDENT_ROLE)
def create_question(request, course_id):
    course_obj = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        creator = request.user.username
        question = Question.objects.create(title=title, body=body, creator=creator, course=course_obj)
        return redirect('view_question', question_id=question.id)
    return redirect(request, 'course', course_id=course_id)

# Student context end


# Multi context start

@role_required(STUDENT_TEACHER_ROLE)
def home(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    if validate_role(request.user, STUDENT_ROLE):
        # Check if student uploaded the necessary amount of files and didn't redeem a scholarship yet
        files_count = len(File.objects.filter(uploader=request.user.username))
        scholarship = Scholarship.objects.filter(student=request.user.username).exists()
        if files_count >= 20 and not scholarship:
            context.update({'scholarship': True})
    return render(request, 'university/home.html', context)


@login_required
def download_file(request, file_id):
    file = File.objects.get(id=file_id)
    response = HttpResponse(file.file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={file.filename}'
    return response


@login_required
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


@role_required(STUDENT_ROLE)
def redeem_scholarship(request):
    scholarship = Scholarship.objects.create(student=request.user.username)
    scholarship.save()
    return redirect('home')


@login_required
def course(request, course_id):
    # Query the course with the given course_id
    course_obj = get_object_or_404(Course, id=course_id)
    # Query the files related to the course
    files = File.objects.filter(course=course_obj)
    # Query the questions related to the course
    questions = Question.objects.filter(course=course_obj)
    # Render the course template with the course and its related files as context

    context = {
        'course': course_obj,
        'course_id': course_obj.id,
        'files': files,
        'questions': questions,
    }
    return render(request, 'university/course.html', context)


@role_required(STUDENT_TEACHER_ROLE)
def view_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question).order_by('timestamp')
    context = {
        'question': question,
        'answers': answers
    }
    return render(request, 'university/view_question.html', context)


@role_required(STUDENT_TEACHER_ROLE)
def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    # Check if the user is allowed to delete the question
    if validate_role(request.user, TEACHER_ROLE) or question.creator == request.user.username:
        question.delete()
    return redirect('course', course_id=question.course.id)


@role_required(STUDENT_TEACHER_ROLE)#לפני הכניסה לפונקציה נבדוק באיזה רול אנחנו נכנסים 
def answer_question(request, question_id): 
    question = get_object_or_404(Question, id=question_id) 
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        answer = form.save(commit=False)
        answer.creator = request.user
        answer.question = question
        answer.save()
        return redirect('view_question', question_id=question_id)


@role_required(STUDENT_TEACHER_ROLE)
def view_appointments(request):
    if validate_role(request.user, STUDENT_ROLE):
        appointments = Appointment.objects.filter(student=request.user.username)
    else:
        appointments = Appointment.objects.filter(teacher=request.user.username)
    return render(request, 'university/view_appointments.html', {'appointments': appointments})


def index(request):
    return render(request, 'university/index.html')




def login(request):
    """Handles the login of users and redirects them to their respective home pages"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login_user(request, user)
            return redirect('admin_home' if user.is_superuser else 'home')
        else:
            messages.warning(request, 'Invalid username or password')
    return render(request, 'university/login.html')


@login_required
def logout(request):
    logout_user(request)
    return redirect('index')


def signup(request):
    """Handles the user registration form and creates a new user"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            group = Group.objects.get(name=form.cleaned_data.get('role'))
            user.groups.add(group)
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login_user(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'university/signup.html', {'form': form})


# Multi context end