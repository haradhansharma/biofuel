from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, NotificationSettings

# This receiver function is meant to be connected to the 'post_save' signal of the User model.
# It automatically creates or updates a corresponding user profile whenever a new user is created or an existing user is saved.

# @receiver(post_save, sender=User)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     """
#     Creates or updates a user profile associated with the User model.

#     Args:
#         sender (Model): The model class that sent the signal (User in this case).
#         instance (User): The specific instance of the User model that was saved.
#         created (bool): Indicates whether a new instance was created or an existing one was saved.
#         **kwargs: Additional keyword arguments passed along with the signal.

#     Returns:
#         None
#     """
#     if not hasattr(instance, 'notificationsettings'):
#         NotificationSettings.objects.create(user=instance)
        
#     if created:
#         # If a new user instance was created, create a corresponding user profile.
#         Profile.objects.create(user=instance)
#         NotificationSettings.objects.create(user=instance)
        
#     else:
#         # If an existing user instance was saved, update the associated user profile.
#         instance.profile.save()
#         instance.notificationsettings.save()
        
        
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):   
    try:
        notificationsettings = instance.notificationsettings  # Attempt to access the related Story
    except NotificationSettings.DoesNotExist:
        notificationsettings = None

    if created or notificationsettings is None:
        # Create a new Story or update the existing one
        notificationsettings, created = NotificationSettings.objects.get_or_create(user=instance)
    
    # Now, make sure that the instance.story is set properly
    if instance.pk != notificationsettings.pk:
        instance.story = notificationsettings
        instance.save()
        

# The following code connects the 'create_or_update_user_profile' function to the 'post_save' signal of the User model.
# Whenever a User instance is saved, this function will be triggered to create or update the associated profile.

# Example usage:
# post_save.connect(create_or_update_user_profile, sender=User)

# Note: You need to connect this signal in your app's signals.py or a similar location for it to work.
