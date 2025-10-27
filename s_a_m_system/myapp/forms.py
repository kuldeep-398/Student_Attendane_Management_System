from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Attendance, Student,Subject

class RegisterForm(UserCreationForm):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'full_name', 'email', 'subject', 'role', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Remove password help texts
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        
        # Optional: remove username help text too
        self.fields['username'].help_text = ''

        # Customize labels
        self.fields['first_name'].label = "First Name"
        self.fields['last_name'].label = "Last Name"
        self.fields['full_name'].label = "Full Name (for Admin)"
        self.fields['subject'].label = "Subject"


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
