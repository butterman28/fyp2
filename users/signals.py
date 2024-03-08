import profile
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=User)
def create_disprofile(sender, instance, created, **kwargs):
    if created:
        disabilityProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def create_samprofile(sender, instance, created, **kwargs):
    if created:
        samaritanProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_disprofile(sender, instance, created, **kwargs):
    instance.disabilityprofile.save()


@receiver(post_save, sender=User)
def save_samprofile(sender, instance, created, **kwargs):
    instance.samaritanprofile.save()
