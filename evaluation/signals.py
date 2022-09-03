from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from doc.models import ExSite
from .models import *
from accounts.models import User, UserType
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import send_mass_mail
from django.db import transaction

import logging
log =  logging.getLogger('log')

'''
Check manytomany field commited
'''
def on_transaction_commit(func):
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))
    return inner

'''
Delete option set related to the logical string when logical string deleted
'''
@receiver(post_delete, sender=LogicalString)
def save_user_profile(sender, instance, **kwargs):    
    OptionSet.objects.filter(ls_id = instance.id).delete()

'''
Recreate all optionset based on logical string .
'''
@receiver(post_save, sender=LogicalString)
@on_transaction_commit
def save_user_profile(sender, instance, **kwargs):
    log.info('Collecting saved logical strings from the admin backend!')
    logical_strings = sender.objects.all()
    log.info(f'{logical_strings.count()} saved logical strings found! ')
    
    logical_options = []
    for logical_string in logical_strings:
        ls_id = logical_string.id
        text = logical_string.text
        overall = logical_string.overall
        positive = logical_string.positive
        option_list = logical_string.option_list
        logical_options.append(option_list)   
        try:
            '''
            edit if any changed
            '''
            option_set = OptionSet.objects.get(option_list = option_list)
            option_set.id = ls_id
            option_set.text = text
            option_set.overall = overall
            option_set.positive = positive
            option_set.save()
        except Exception as e:
            '''
            delete changed to re input
            '''
            lo_except_last = [x for x in logical_options if x != option_list]
            unmatched = [item for item in logical_options if not item in lo_except_last ]
            try:
                for u in unmatched:
                    try:
                        OptionSet.objects.get(option_list = u).delete()
                    except:
                        continue
            except Exception as e:
                continue
            new_option_set = OptionSet(option_list = option_list, text = text, overall = overall , positive = positive, ls_id = ls_id )
            new_option_set.save()
    
    





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
                
