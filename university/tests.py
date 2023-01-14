from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .constants import STUDENT_ROLE, TEACHER_ROLE
from .models import Course, Appointment, File, Answer, Scholarship, Question

User = get_user_model()


class ViewsTests(TestCase):
    def setUp(self):
        # Create test users
        self.default_password = 'password'

        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password=self.default_password
        )
        self.teacher = User.objects.create_user(
            username='teacher',
            email='teacher@example.com',
            password=self.default_password
        )
        self.student = User.objects.create_user(
            username='student',
            email='student@example.com',
            password=self.default_password
        )

        # Add users to respective groups, note that admin is not a group but a default superuser
        teacher_group, _ = Group.objects.get_or_create(name=TEACHER_ROLE)
        teacher_group.user_set.add(self.teacher)
        student_group, _ = Group.objects.get_or_create(name=STUDENT_ROLE)
        student_group.user_set.add(self.student)

        # Create test courses
        self.course = Course.objects.create(
            name='Test Course 1',
            category='Test Category 1'
        )

        # Create test files
        self.teacher_file = File.objects.create(
            filename='Test File 1',
            file=SimpleUploadedFile('test_file_1.txt', b'test'),
            uploader=self.teacher.username,
            teacher_file=True,
            course=self.course
        )
        self.student_file = File.objects.create(
            filename='Test File 2',
            file=SimpleUploadedFile('test_file_2.txt', b'test'),
            uploader=self.student.username,
            teacher_file=False,
            course=self.course
        )

        # Create test questions
        self.question = Question.objects.create(
            title='Test Question 1',
            body='Test question body 1',
            course=self.course,
            creator=self.student
        )

        # Create test answers
        self.student_answer = Answer.objects.create(
            creator=self.student,
            question=self.question,
            body='Test answer body 1'
        )
        self.teacher_answer = Answer.objects.create(
            creator=self.teacher,
            question=self.question,
            body='Test answer body 2'
        )

        # Create test appointments
        self.appointment = Appointment.objects.create(
            time='2023-10-10',
            teacher=self.teacher,
            student=self.student,
            zoom_link='https://zoom.us/123'
        )

    def tearDown(self):
        """Cleand models from database before each test"""
        User.objects.all().delete()
        Course.objects.all().delete()
        Question.objects.all().delete()
        Answer.objects.all().delete()
        Appointment.objects.all().delete()
        Scholarship.objects.all().delete()
        for file in File.objects.all():
            # Deletes both the actual file in storage and the file object from the database
            file.file.delete()
            file.delete()

    def test_login(self):
        """Test login for all user types"""
        # Admin login test.
        # Test correct credentials
        self.client.login(username=self.admin.username, password=self.default_password)
        response = self.client.get(reverse('admin_home'))
        self.assertEqual(response.status_code, 200)
        # Admin logout test
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

        # Test incorrect credentials
        self.client.login(username=self.admin, password='wrong')
        response = self.client.get(reverse('admin_home'))
        self.assertEqual(response.status_code, 302)

        # Teacher login test.
        # Test correct credentials
        self.client.login(username=self.teacher.username, password=self.default_password)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Teacher Logout test
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

        # Test incorrect credentials
        self.client.login(username=self.teacher, password='wrong')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

        # Student login test.
        # Test correct credentials
        self.client.login(username=self.student.username, password=self.default_password)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Student Logout test
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

        # Test incorrect credentials
        self.client.login(username=self.student, password='wrong')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)

    def test_admin_course_creation(self):
        """Test course creation by an admin"""
        # Login as admin
        self.client.login(username=self.admin.username, password=self.default_password)

        # Test course creation with correct data
        response = self.client.post(reverse('add_course'), data={'name': 'Test Course', 'category': 'Test Category'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(Course.objects.last().name, 'Test Course')

        # Test course creation with incorrect data
        response = self.client.post(reverse('add_course'), data={'name': '', 'category': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Course.objects.count(), 2)
        self.client.logout()

    def test_admin_course_editing(self):
        """Test course editing"""
        # Login as admin
        login_response = self.client.post(
            reverse('login'),
            data={'username': self.admin, 'password': self.default_password},
            follow=True
        )
        self.assertEqual(login_response.status_code, 200)

        # Test course editing
        response = self.client.post(reverse('edit_course', args=[self.course.id]), data={'name': 'Course 2', 'category': 'Category 2'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Course.objects.get(id=1).name, 'Course 2')
        self.assertEqual(Course.objects.get(id=1).category, 'Category 2')
        self.client.logout()

    def test_admin_course_deletion(self):
        """Test course deletion"""
        # Log in as admin
        self.client.login(username=self.admin.username, password=self.default_password)

        # Send POST request to delete a course
        response = self.client.get(reverse('delete_course', args=[self.course.id]))

        # Check that the course was deleted successfully
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Course.objects.count(), 0)
        self.client.logout()

    def test_admin_file_deletion(self):
        """Test file deletion by an admin user"""
        # Log in as admin
        self.client.login(username=self.admin.username, password=self.default_password)
        # Delete file
        response = self.client.post(reverse('delete_file', args=[self.teacher_file.id]))
        # Check that user was redirected to admin home
        self.assertRedirects(response, reverse('admin_home'))

        # Check that file is deleted (asserting 1 because 2 exist before deletion)
        self.assertEqual(File.objects.count(), 1)

        # Check that trying to delete a file that doesn't exist returns a 404 error
        response = self.client.post(reverse('delete_file', args=[self.teacher_file.id]))
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_teacher_file(self):
        """Tests file upload and deletion as a teacher"""
        # login as a teacher
        self.client.login(username=self.teacher.username, password=self.default_password)
        # Test file upload
        response = self.client.post(reverse('upload_file', args=[self.course.id]), data={
            'filename': 'test.txt',
            'file': SimpleUploadedFile('test.txt', b'test'),
            'teacher_file': True,
            'course': self.course,
        })
        self.assertRedirects(response, reverse('course', args=[self.course.id]))

        # Check that file was created
        file1 = File.objects.get(filename='test.txt')
        self.assertEqual(file1.uploader, self.teacher.username)
        self.assertEqual(file1.teacher_file, True)
        self.assertEqual(file1.course, self.course)

        # Test file deletion
        file_id = self.teacher_file.id
        response = self.client.get(reverse('delete_file', args=[file_id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(File.objects.filter(id=file_id).exists())
        self.client.logout()

    def test_teacher_appointment(self):
        """Tests teacher appointment creation and deletion"""
        # Ensure that a teacher can create an appointment
        self.client.login(username=self.teacher.username, password=self.default_password)
        response = self.client.post(reverse('create_appointment'), data={
            'time': '2023-12-01',
            'teacher': self.teacher.username,
            'student': self.student.username,
            'zoom_link': 'https://zoom.com/appointments/12345'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Appointment.objects.filter(student=self.student.username).exists())

        # Send request to delete appointment
        response = self.client.get(reverse('delete_appointment', args=[self.appointment.id]))
        # Check that appointment1 was deleted
        self.assertFalse(Appointment.objects.filter(id=self.appointment.id).exists())
        # Check redirect
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    def test_teacher_question_answer(self):
        """Test that a teacher can answer questions"""
        # Login as teacher
        self.client.login(username=self.teacher.username, password=self.default_password)

        # Check that there are 2 answers for question
        self.assertEqual(Answer.objects.filter(question=self.question).count(), 2)

        # Send POST request to create answer
        response = self.client.post(
            reverse('answer_question', args={self.question.id}),
            data={'body': 'This is an answer'},
            follow=True
        )

        # Check that one answer was created
        self.assertEqual(Answer.objects.filter(question=self.question).count(), 3)
        # Check redirect
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_student_file(self):
        """Test student file upload and deletion"""
        # log student in
        self.client.login(username=self.student.username, password=self.default_password)
        # upload student file
        response = self.client.post(reverse('upload_file', args=[self.course.id]), data={
            'filename': 'file1',
            'file': SimpleUploadedFile('file_student.txt', b'file_content'),
            'teacher_file': 'False',
            'course': self.course.id,
        }, follow=True)
        # check if file was uploaded
        self.assertEqual(response.status_code, 200)
        self.assertEqual(File.objects.count(), 3)

        # Send request to delete student file
        response = self.client.get(reverse('delete_file', args=[self.student_file.id]))
        self.assertEqual(response.status_code, 302)

        # Check that the student file was deleted
        self.assertFalse(File.objects.filter(id=self.student_file.id).exists())
        self.assertEqual(File.objects.count(), 2)
        self.client.logout()

    def test_student_question_creation(self):
        """Test student asking/creating a question"""
        # Login student
        self.client.login(username=self.student.username, password=self.default_password)
        # Send POST request to create student question
        data = {
            'title': 'Test Question created',
            'body': 'Test question body',
            'course': self.course,
        }
        response = self.client.post(reverse('create_question', args=[self.course.id]), data=data)
        self.assertEqual(response.status_code, 302)

        # Check if student question was created
        self.assertTrue(Question.objects.filter(title='Test Question created').exists())

        # check that the student user has 1 question
        response = self.client.get(reverse('course', args=[self.course.id]))
        self.assertEqual(len(response.context['questions']), 2)

        # delete the question
        self.client.post(reverse('delete_question', args=[self.question.id]))

        # check that the student user has no questions
        response = self.client.get(reverse('course', args=[self.course.id]))
        self.assertEqual(len(response.context['questions']), 1)
        self.client.logout()

    def test_scholarship(self):
        self.client.login(username=self.student.username, password=self.default_password)

        # Go to home page, student shouldn't have a scholarship
        response = self.client.get(reverse('home'))
        self.assertFalse(response.context.get('scholarship', False))

        # Upload 20 files
        for i in range(20):
            self.client.post(reverse('upload_file', args=[self.course.id]), data={
                'filename': f'file{i}',
                'file': SimpleUploadedFile(f'file{i}.txt', b'file_content'),
                'teacher_file': 'False',
                'course': self.course,
            }, follow=True)

        # Go to home page after uploading 20 files and scholarship should be true
        response = self.client.get(reverse('home'))
        self.assertTrue(response.context['scholarship'])
        self.client.logout()
