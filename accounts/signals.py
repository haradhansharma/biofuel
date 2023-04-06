from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


# During signup system will fill profile table autometically by signal to create user profile.
@receiver(post_save, sender=User)
def cup(sender, instance, created, **kwargs):
    
    if created:        
        Profile.objects.create(user=instance)        
    else:        
        instance.profile.save()  
    
        

