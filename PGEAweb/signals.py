from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Usuario, Alumno, Maestra

@receiver(post_save, sender=Usuario)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'alumno':
            Alumno.objects.create(user=instance)
        elif instance.role == 'maestra':
            Maestra.objects.create(user=instance)
