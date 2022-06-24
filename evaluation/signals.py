from django.db.models.signals import post_save, pre_save
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
        staffs = User.objects.filter(is_staff = True, is_superuser = True)
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
        send_mass_mail((mail_to_staff), fail_silently=False)
        send_mass_mail((mail_to_producer), fail_silently=False)
        

        
        
@receiver(pre_save, sender=Option)
def on_change(sender, instance, **kwargs):
    if instance.id is None: # new object will be created
        pass 
    else:
        # get unchanged item
        previous = sender.objects.get(id=instance.id)
        if previous.statement != instance.statement or previous.next_step != instance.next_step  : # field will be updated
            #We will take which is not pending as pending will be update autometically when try to notify and create new one
            notifiyed_evaluator = Evaluator.objects.filter(feedback_updated = True)
            # Will track all feedback of this option in the databse
            evastatements = EvaLebelStatement.objects.filter(option_id = instance.id)
            #will update all report or evaluator which is upodate pending when changes happend in the statement and in the next step of option.
            for evastatement in evastatements:
                current_evaluator = evastatement.evaluator
                if current_evaluator in notifiyed_evaluator:
                    if evastatement.statement != previous.statement or evastatement.next_step != previous.next_step:
                        current_evaluator.feedback_updated = False
                        current_evaluator.save()
                    else:
                        pass
                else:
                    pass
                        
                    
        
       
