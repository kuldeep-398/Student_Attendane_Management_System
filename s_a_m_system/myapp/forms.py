from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Attendance, Student,Subject

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control'
    }))

class AttendanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        students = kwargs.pop('students')
        super().__init__(*args, **kwargs)
        for student in students:
            self.fields[f'student_{student.id}'] = forms.ChoiceField(
                choices=[('P', 'Present'), ('A', 'Absent')],
                label=student.user.username,
                widget=forms.RadioSelect
            )


# forms.py
class TeacherForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'is_approved']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'roll_no', 'course']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'teachers', 'students']
        widgets = {
            'teachers': forms.CheckboxSelectMultiple,
            'students': forms.CheckboxSelectMultiple,
        }




class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['roll_no', 'course']
