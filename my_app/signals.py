from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee

@receiver(post_save, sender=Employee)
def employee_created(sender, instance, created, **kwargs):
    if created:
        # Here you can perform the actions you want when a new employee is created.
        # For example, you can log a message, send an email, or trigger any other function.
        print(f"New employee created: {instance.name} (ID: {instance.id})")
