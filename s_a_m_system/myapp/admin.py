from django.contrib import admin
from .models import CustomUser, Student, Attendance

admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Attendance)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'role', 'roll_no', 'subject')
#     search_fields = ('user__username', 'user__email')
