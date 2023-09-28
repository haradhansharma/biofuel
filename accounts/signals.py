from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, NotificationSettings

# This receiver function is meant to be connected to the 'post_save' signal of the User model.
# It automatically creates or updates a corresponding user profile whenever a new user is created or an existing user is saved.

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Creates or updates a user profile associated with the User model.

    Args:
        sender (Model): The model class that sent the signal (User in this case).
        instance (User): The specific instance of the User model that was saved.
        created (bool): Indicates whether a new instance was created or an existing one was saved.
        **kwargs: Additional keyword arguments passed along with the signal.

    Returns:
        None
    """
        
    if created:
        # If a new user instance was created, create a corresponding user profile.
        Profile.objects.create(user=instance)        
    else:
        # If an existing user instance was saved, update the associated user profile.
        instance.profile.save()

        
        
@receiver(post_save, sender=User)
def create_or_update_notification_settings(sender, instance, created, **kwargs):  
    """
    Creates or updates a notification setting associated with the User model.
    As it has been created after existing user so e are taking creating notification if not yet to avoid error

    Args:
        sender (Model): The model class that sent the signal (User in this case).
        instance (User): The specific instance of the User model that was saved.
        created (bool): Indicates whether a new instance was created or an existing one was saved.
        **kwargs: Additional keyword arguments passed along with the signal.

    Returns:
        None
    """ 
    try:
        notificationsettings = instance.notificationsettings  # Attempt to access the related Story
    except NotificationSettings.DoesNotExist:
        notificationsettings = None

    if created or notificationsettings is None:
        # Create a notification settings or update the existing one
        notificationsettings, created = NotificationSettings.objects.get_or_create(user=instance)
    
    # Now, make sure that the instance.notificationsettings is set properly
    if instance.pk != notificationsettings.pk:
        instance.story = notificationsettings
        instance.save()
        


