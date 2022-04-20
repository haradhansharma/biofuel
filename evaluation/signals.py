from django.db.models.signals import post_save
from django.dispatch import receiver

from doc.models import ExSite
from .models import *
from accounts.models import User, UserType
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import send_mass_mail


'''
sending mail to the staff and producer after update of question

'''
@receiver(post_save, sender=Question)
def question_update_mail(sender, instance, **kwargs):
    if instance.is_active:
        producers = UserType.objects.get(is_producer = True)
        current_site = Site.objects.get_current()
        staffs = User.objects.filter(is_staff = True)
        producers = User.objects.filter(type = producers)
        subject = 'Question updated!'                  
                
        # load a template like get_template() 
        # and calls its render() method immediately.
        # pass the parameter to the template
        message = render_to_string('emails/question_updated.html', {
            'instance': instance,              
            'domain': current_site.domain,            
        }) 
        
        site = ExSite.on_site.get()          
        
        
        #Send multi mail with single conenction
        mail_to_staff = [(subject, message, site.email, [staff]) for staff in staffs]
        mail_to_producer = [(subject, message, site.email, [producer]) for producer in producers]  
        # send_mass_mail((mail_to_staff), fail_silently=False)
        # send_mass_mail((mail_to_producer), fail_silently=False)
        
        
       
