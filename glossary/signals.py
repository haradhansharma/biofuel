from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *
# from django.core.exceptions import ValidationError
from django import forms




        

@receiver(post_save, sender=GRequests)
def make_glossary(sender, instance, created, *args, **kwargs):
    if created:
        pass   
    else:        
         
        
        Glossary.objects.create(title = instance.title, description = instance.description)
        instance.delete()     