from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .constants import STUDENT_ROLE, TEACHER_ROLE
from .models import Course, Appointment, File, Answer, Scholarship, Question

User = get_user_model()

class ViewsTests(TestCase):

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