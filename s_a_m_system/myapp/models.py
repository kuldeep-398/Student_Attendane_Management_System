from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# ---- Custom User ----
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_approved = models.BooleanField(default=False)
    subject = models.ForeignKey('Subject', null=True, blank=True, on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# ---- Student ----
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20)
    course = models.CharField(max_length=50)

    

    def __str__(self):
        return f"{self.user.username} - {self.roll_no}"


# ---- Subject ----
class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    teachers = models.ManyToManyField(
        CustomUser,
        related_name='subjects_taught',
        limit_choices_to={'role': 'teacher'},
        blank=True
    )
    students = models.ManyToManyField(
        CustomUser,
        related_name='subjects_enrolled',
        limit_choices_to={'role': 'student'},
        blank=True
    )

    def __str__(self):
        return self.name


# ---- Attendance ----
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('P', 'Present'),
        ('A', 'Absent'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    marked_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='marked_attendance')

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name} - {self.date} - {self.status}"
