from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Custom dashboards
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),

    # CRUD-admin [Teachers]
    path('admins/teachers/', views.admin_teachers, name='admin_teachers'),
    path('admins/teachers/add/', views.admin_add_teacher, name='admin_add_teacher'),
    path('admins/teachers/edit/<int:teacher_id>/', views.admin_edit_teacher, name='admin_edit_teacher'),
    path('admins/teachers/delete/<int:teacher_id>/', views.admin_delete_teacher, name='admin_delete_teacher'),
    path('admins/teachers/approve/<int:teacher_id>/', views.admin_approve_teacher, name='admin_approve_teacher'),
    
    # Admin CRUD: [Students]
    path('admins/students/', views.admin_students, name='admin_students'),
    path('admins/students/add/', views.admin_add_student, name='admin_add_student'),
    path('admins/students/edit/<int:student_id>/', views.admin_edit_student, name='admin_edit_student'),
    path('admins/students/delete/<int:student_id>/', views.admin_delete_student, name='admin_delete_student'),

    # Admin CRUD: [Subjects]
    path('admins/subjects/', views.admin_subjects, name='admin_subjects'),
    path('admins/subjects/<int:subject_id>/', views.admin_subject_detail, name='admin_subject_detail'),
    path('admins/subjects/add/', views.admin_add_subject, name='admin_add_subject'),
    path('admins/subjects/edit/<int:subject_id>/', views.admin_edit_subject, name='admin_edit_subject'),
    path('admins/subjects/delete/<int:subject_id>/', views.admin_delete_subject, name='admin_delete_subject'),

    # Teacher CRUD [Attendance Dashboard]
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/subject/<int:subject_id>/attendance/', views.mark_attendance, name='mark_attendance'),
    path('teacher/subject/<int:subject_id>/add_student/', views.admin_add_student, name='admin_add_student'),



]
