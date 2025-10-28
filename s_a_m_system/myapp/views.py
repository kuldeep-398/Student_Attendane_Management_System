from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import CustomUser, Student, Attendance
from .forms import RegisterForm, LoginForm, Subject, SubjectForm
from datetime import datetime
from django.db.models import Count

# ------------------------------
# Home Page
# ------------------------------
def home(request):
    return render(request, 'home.html')

# ------------------------------
# Register Page
# ------------------------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            subject = form.cleaned_data.get('subject')
            name = form.cleaned_data.get('name')

            if role == 'admin':
                user.first_name = name
                user.last_name = ''
                user.subject = None
            else:
                user.subject = subject

            if user.role == 'teacher':
                user.is_approved = False
            else:
                user.is_approved = False

            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# ------------------------------
# Login Page
# ------------------------------
def login_view(request):
    form = LoginForm(request.POST or None)
    error = None

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_approved:
            login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            error = "Invalid credentials or account not approved yet."

    return render(request, 'login.html', {'form': form, 'error': error})

# ------------------------------
# Logout
# ------------------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# ------------------------------
# Admin Dashboard (Approve Teachers)
# ------------------------------
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('home')

    pending_teachers = CustomUser.objects.filter(role='teacher', is_approved=False)
    total_teachers = CustomUser.objects.filter(role='teacher').count()
    total_students = CustomUser.objects.filter(role='student').count()
    total_subjects = Subject.objects.count()
    total_users = total_teachers + total_students

    if request.method == 'POST':
        teacher_id = request.POST.get('approve_id')
        teacher = CustomUser.objects.get(id=teacher_id)
        teacher.is_approved = True
        teacher.save()

    return render(request, 'admin/admin_dashboard.html', {
        'pending_teachers': pending_teachers,
        'total_teachers': total_teachers,
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_users': total_users
    })

# ------------------------------
# Admin - Teacher CRUD
# ------------------------------
@login_required
def admin_teachers(request):
    if request.user.role != 'admin':
        return redirect('home')
    teachers = CustomUser.objects.filter(role='teacher')
    return render(request, 'admin/admin_teachers.html', {'teachers': teachers})

@login_required
def admin_add_teacher(request):
    if request.user.role != 'admin':
        return redirect('home')

    subject_id = request.GET.get('subject_id')  # Get subject_id from query param

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.role = 'teacher'
            teacher.is_approved = True
            teacher.save()

            if subject_id:
                subject = Subject.objects.get(id=subject_id)
                subject.teachers.add(teacher)

            return redirect('admin_subject_detail', subject_id=subject_id) if subject_id else redirect('admin_teachers')
    else:
        form = RegisterForm()
    return render(request, 'admin/admin_add_teacher.html', {'form': form})

@login_required
def admin_edit_teacher(request, teacher_id):
    if request.user.role != 'admin':
        return redirect('home')
    teacher = CustomUser.objects.get(id=teacher_id, role='teacher')
    if request.method == 'POST':
        form = RegisterForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('admin_teachers')
    else:
        form = RegisterForm(instance=teacher)
    return render(request, 'admin/admin_edit_teacher.html', {'form': form, 'teacher': teacher})

@login_required
def admin_delete_teacher(request, teacher_id):
    if request.user.role != 'admin':
        return redirect('home')
    teacher = CustomUser.objects.get(id=teacher_id, role='teacher')
    if request.method == 'POST':
        teacher.delete()
        return redirect('admin_teachers')
    return redirect('admin_teachers')

@login_required
def admin_approve_teacher(request, teacher_id):
    if request.user.role != 'admin':
        return redirect('home')
    teacher = CustomUser.objects.get(id=teacher_id, role='teacher')
    if request.method == 'POST':
        teacher.is_approved = True
        teacher.save()
    return redirect('admin_teachers')

# ------------------------------
# Admin - Student CRUD
# ------------------------------
@login_required
def admin_students(request):
    if request.user.role != 'admin':
        return redirect('home')
    students = CustomUser.objects.filter(role='student')
    return render(request, 'admin/admin_students.html', {'students': students})

@login_required
def admin_add_student(request):
    if request.user.role not in ['admin', 'teacher']:
        return redirect('home')

    subject_id = request.GET.get('subject_id')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.role = 'student'
            student.save()

            if subject_id:
                subject = Subject.objects.get(id=subject_id)
                subject.students.add(student)

            if request.user.role == 'admin':
                return redirect('admin_subject_detail', subject_id=subject_id) if subject_id else redirect('admin_students')
            else:  # teacher
                return redirect('teacher_dashboard')
    else:
        form = RegisterForm()
    return render(request, 'admin/admin_add_student.html', {'form': form, 'subject_id': subject_id})

@login_required
def admin_approve_student(request, student_id):
    if request.user.role != 'admin':
        return redirect('home')
    student = CustomUser.objects.get(id=student_id, role='student')
    if request.method == 'POST':
        student.is_approved = True
        student.save()
    return redirect('admin_students')

@login_required
def admin_edit_student(request, student_id):
    if request.user.role != 'admin':
        return redirect('home')
    student = CustomUser.objects.get(id=student_id, role='student')
    if request.method == 'POST':
        form = RegisterForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('admin_students')
    else:
        form = RegisterForm(instance=student)
    return render(request, 'admin/admin_edit_student.html', {'form': form, 'student': student})

@login_required
def admin_delete_student(request, student_id):
    if request.user.role != 'admin':
        return redirect('home')
    student = CustomUser.objects.get(id=student_id, role='student')
    if request.method == 'POST':
        student.delete()
        return redirect('admin_students')
    return redirect('admin_students')

# ------------------------------
# Admin - Subject CRUD
# ------------------------------
@login_required
def admin_subjects(request):
    if request.user.role != 'admin':
        return redirect('home')
    subjects = Subject.objects.prefetch_related('teachers', 'students').all()
    return render(request, 'admin/admin_subjects.html', {'subjects': subjects})

@login_required
def admin_add_subject(request):
    if request.user.role != 'admin':
        return redirect('home')
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_subjects')
    else:
        form = SubjectForm()
    return render(request, 'admin/admin_add_subject.html', {'form': form})

@login_required
def admin_edit_subject(request, subject_id):
    if request.user.role != 'admin':
        return redirect('home')
    subject = Subject.objects.get(id=subject_id)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            return redirect('admin_subjects')
    else:
        form = SubjectForm(instance=subject)
    return render(request, 'admin/admin_edit_subject.html', {'form': form, 'subject': subject})

@login_required
def admin_delete_subject(request, subject_id):
    if request.user.role != 'admin':
        return redirect('home')
    subject = Subject.objects.get(id=subject_id)
    if request.method == 'POST':
        subject.delete()
        return redirect('admin_subjects')
    return redirect('admin_subjects')

@login_required
def admin_subject_detail(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == "POST":
        # -------------------------------
        # ADD and REMOVE TEACHER
        # -------------------------------
        if "add_teacher" in request.POST:
            teacher_id = request.POST.get("teacher_id")
            teacher = get_object_or_404(CustomUser, id=teacher_id, role="teacher")
            subject.teachers.add(teacher)

        elif "remove_teacher" in request.POST:
            teacher_id = request.POST.get("teacher_id")
            teacher = get_object_or_404(CustomUser, id=teacher_id, role="teacher")
            subject.teachers.remove(teacher)

        # -------------------------------
        # ADD and REMOVE STUDENT
        # -------------------------------
        elif "add_student" in request.POST:
            student_user_id = request.POST.get("student_id")
            student_user = get_object_or_404(CustomUser, id=student_user_id, role="student")
            subject.students.add(student_user)

        elif "remove_student" in request.POST:
            student_user_id = request.POST.get("student_id")
            student_user = get_object_or_404(CustomUser, id=student_user_id, role="student")
            subject.students.remove(student_user)

        return redirect("admin_subject_detail", subject_id=subject.id)

    teachers = subject.teachers.filter(role="teacher")
    students = subject.students.filter(role="student")
    available_teachers = CustomUser.objects.filter(role="teacher").exclude(id__in=teachers)
    available_students = CustomUser.objects.filter(role="student").exclude(id__in=students)

    return render(
        request,
        "admin/admin_subject_detail.html",
        {
            "subject": subject,
            "teachers": teachers,
            "students": students,
            "available_teachers": available_teachers,
            "available_students": available_students,
        },
    )

# ------------------------------
# Teacher Dashboard
# ------------------------------
@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('home')

    subjects = Subject.objects.filter(teachers=request.user)

    return render(request, 'teacher/teacher_dashboard.html', {'subjects': subjects})

# ------------------------------
# Mark / Update Attendance
# ------------------------------
@login_required
def mark_attendance(request, subject_id):
    if request.user.role != 'teacher':
        return redirect('home')

    subject = get_object_or_404(Subject, id=subject_id, teachers=request.user)

    students = Student.objects.filter(user__in=subject.students.all())
    today = timezone.now().date()

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status in ['P', 'A']:

                Attendance.objects.update_or_create(
                    student=student,
                    subject=subject,
                    date=today,
                    defaults={'status': status, 'marked_by': request.user}
                )
        return redirect('teacher_dashboard')

    attendance_dict = {}
    for student in students:
        attendance = Attendance.objects.filter(
            student=student,
            subject=subject,
            date=today,
            marked_by=request.user
        ).first()
        attendance_dict[student.id] = attendance.status if attendance else ''

    return render(request, 'teacher/mark_attendance.html', {
        'subject': subject,
        'students': students,
        'attendance_dict': attendance_dict,
        'today': today
    })

# ------------------------------
# Student Dashboard (View Attendance Report)
# ------------------------------
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from .models import Attendance, Subject, Student

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('home')
    
    student = get_object_or_404(Student, user=request.user)
    
    subjects = Subject.objects.filter(students=request.user)
    
    selected_subject_id = request.GET.get('subject_id')
    selected_subject = None
    if selected_subject_id:
        selected_subject = get_object_or_404(Subject, id=selected_subject_id)
    elif subjects.exists():
        selected_subject = subjects.first()
    
    date_str = request.GET.get('date')
    if date_str:
        try:
            selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            selected_date = timezone.now().date()
    else:
        selected_date = timezone.now().date()
    
    attendance_records = Attendance.objects.filter(
        student=student, subject=selected_subject
    ).order_by('-date') if selected_subject else Attendance.objects.none()
    attendance_records = attendance_records.filter(date__lte=selected_date)

    current_month = timezone.now().month
    current_year = timezone.now().year
    monthly_attendance = Attendance.objects.filter(
        student=student, subject=selected_subject, date__month=current_month, date__year=current_year
    )
    present_count = monthly_attendance.filter(status='P').count()
    absent_count = monthly_attendance.filter(status='A').count()
    total_days = present_count + absent_count
    percentage = round((present_count / total_days) * 100, 2) if total_days > 0 else 0
    
    return render(request, 'student/student_dashboard.html', {
        'attendance': attendance_records,
        'percentage': percentage,
        'subjects': subjects,
        'selected_subject_id': selected_subject.id if selected_subject else None,
        'selected_date': selected_date,
        'present_count': present_count,
        'absent_count': absent_count,
    })
