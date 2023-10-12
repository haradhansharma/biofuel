# Import necessary modules for working with Django signals.
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Import models and other dependencies.
from .models import *

# Import logging module for creating log entries.
import logging
log =  logging.getLogger('log')

# Define a receiver function to be triggered after saving a GRequests instance.    
@receiver(post_save, sender=GRequests)
def make_glossary(sender, instance, created, *args, **kwargs):
    """
    Receiver function triggered after saving a GRequests instance.

    This function is a signal receiver that gets triggered after a GRequests
    instance is saved. It checks if the instance is newly created (created=True),
    and if not, it creates a Glossary entry based on the GRequests instance and
    then deletes the GRequests instance.

    Args:
        sender: The sender of the signal.
        instance: The instance of the GRequests model.
        created (bool): Indicates whether the GRequests instance was newly created.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.
    """
    if created:
        # If the GRequests instance is newly created, do nothing.
        pass   
    else: 
         # If the GRequests instance is not newly created, create a Glossary entry.
        log.info('Glossary created from request________________')   
        Glossary.objects.create(title = instance.title, description = instance.description)
        
        # Delete the GRequests instance since it's now been converted to a Glossary entry.
        instance.delete()     