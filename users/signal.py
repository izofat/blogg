# pylint: disable=unused-argument
# pylint: disable=relative-beyond-top-level
"""Signals"""
from typing import Any
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender: type, instance: User, **kwargs: Any) -> None:
    """If there is action in user it comes here
    if the profile exist updates profile if not creates it"""

    if hasattr(instance, "profile"):
        instance.profile.save()
    else:
        Profile.objects.create(user=instance)
