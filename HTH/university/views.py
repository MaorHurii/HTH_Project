from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CourseForm, AppointmentForm, AnswerForm
from .models import Course, Appointment, Report, Question, Answer


def index(request):
    return render(request, 'university/index.html')


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_home')
        else:
            messages.warning(request, 'Invalid username or password')
            return redirect('admin_login')
    return render(request, 'university/admin_login.html')

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


@role_required(TEACHER_ROLE)
def view_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'university/view_appointments.html', {'appointments': appointments})


@role_required(TEACHER_ROLE)
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            time = form.cleaned_data['time']
            Appointment.objects.create(student=student, time=time)
            return redirect('view_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'university/create_appointment.html')


def delete_appointment(appointment_id):
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

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('student_home')
        else:
            messages.warning(request, 'Invalid username or password')
            return redirect('student_login')
    return render(request, 'university/student_login.html')


@login_required(login_url='student_login')
def student_logout(request):
    logout(request)
    return redirect('index')


def student_home(request):
    return render(request, 'university/student_home.html')


@login_required(login_url='student_login')
def view_courses(request):
    courses = Course.objects.all()
    return render(request, 'university/view_courses.html', {'courses': courses})


@login_required(login_url='student_login')
def view_questions(request):
    questions = Question.objects.all()
    return render(request, 'university/view_questions.html', {'questions': questions})


@login_required(login_url='student_login')
def create_question(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        Question.objects.create(title=title, description=description)
        return redirect('view_questions')
    return render(request, 'university/create_question.html')


@login_required(login_url='student_login')
def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        filename = file.name
        Report.objects.create(filename=filename, file=file, uploader=request.user.username)
        return redirect('student_home')
    return render(request, 'university/upload_file.html')
