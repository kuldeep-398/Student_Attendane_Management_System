from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Student

@receiver(post_save, sender=CustomUser)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'student':
        # generate a unique roll number
        roll_no = f"STU{instance.id:04d}"
        Student.objects.get_or_create(
            user=instance,
            defaults={'roll_no': roll_no, 'course': 'Undeclared'}
        )
