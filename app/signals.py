
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)  # Create the Profile object

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Save the Profile object if it already exists
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Create the profile if it doesn't exist
        Profile.objects.create(user=instance)

