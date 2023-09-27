from django.conf import settings
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
import json
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
Check manytomany field committed
'''
def on_transaction_commit(func):
    '''
    A decorator to execute a function after a database transaction is committed.
    This ensures that the function is executed only when changes to the database are finalized.
    
    Args:
        func (callable): The function to be executed after the transaction is committed.
    
    Returns:
        callable: A wrapped function.
    '''
    def inner(*args, **kwargs):
        transaction.on_commit(lambda: func(*args, **kwargs))
    return inner

'''
Delete option sets related to the logical string when a logical string is deleted.
'''
@receiver(post_delete, sender=LogicalString)
def delete_option_sets(sender, instance, **kwargs): 
    '''
    A signal handler to delete associated OptionSet objects when a LogicalString is deleted.
    
    Args:
        sender: The sender of the signal (LogicalString).
        instance: The instance of the LogicalString being deleted.
        **kwargs: Additional keyword arguments.
    '''   
    OptionSet.objects.filter(ls_id = instance.id).delete()

'''
Recreate all OptionSets based on LogicalString.
'''
@receiver(post_save, sender=LogicalString)
@on_transaction_commit
def recreate_option_sets(sender, instance, **kwargs):
    '''
    A signal handler to recreate OptionSet objects based on changes in LogicalString.
    
    Args:
        sender: The sender of the signal (LogicalString).
        instance: The instance of the LogicalString being saved.
        **kwargs: Additional keyword arguments.
    '''
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
            Edit if any changed.
            '''
            option_set = OptionSet.objects.get(option_list = option_list)
            option_set.id = ls_id
            option_set.text = text
            option_set.overall = overall
            option_set.positive = positive
            option_set.save()
        except Exception as e:
            '''
            Delete changed to re-input.
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
Assign all questions to the oil during new oil create.
'''
@receiver(post_save, sender=OliList)
def add_auestion_to_the_oil(sender, instance, created, **kwargs):
    '''
    A signal handler to assign all active questions to an oil when a new oil is created.
    
    Args:
        sender: The sender of the signal (OliList).
        instance: The instance of the OliList being saved.
        created (bool): True if a new object is created, False if an existing one is saved.
        **kwargs: Additional keyword arguments.
    '''
    if created:        
        active_questions = Question.objects.filter(is_active = True)        
        stdoil = StdOils.objects.create(select_oil = instance)
        # oil = StdOils.objects.get(id = stdoil.id)
        for question in active_questions:
            try:
                option = Option.objects.filter(question = question)[0]
            except:
                option = None               
            StandaredChart.objects.create(oil = stdoil, question = question, option=option)        

        
        
@receiver(pre_save, sender=Option)
def on_option_change(sender, instance, **kwargs):
    '''
    A signal handler to detect changes in Option objects and notify evaluators accordingly.
    
    Args:
        sender: The sender of the signal (Option).
        instance: The instance of the Option being saved.
        **kwargs: Additional keyword arguments.
    '''
    if instance.id is None: # New object will be created
        pass 
    else:
        # Get the unchanged item
        previous = sender.objects.get(id=instance.id)
        if (
            previous.statement != instance.statement 
            or previous.next_step != instance.next_step
        ) : # Fields will be updated
            # We will take which is not pending as pending will be updated automatically when trying to notify and create a new one
            notifiyed_evaluator = Evaluator.objects.filter(feedback_updated = True)
            # Will track all feedback of this option in the database
            evastatements = EvaLebelStatement.objects.filter(option_id = instance.id)
            # Will update all reports or evaluators which are pending when changes happen in the statement and in the next step of the option.
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
                
                
@receiver(post_save, sender=NextActivities)
def add_to_the_user_next(sender, instance, created, **kwargs):    
    '''
    A signal handler to add a NextActivity to a user's list of upcoming activities.

    Args:
        sender: The sender of the signal (NextActivities).
        instance: The instance of the NextActivities being saved.
        created (bool): True if a new object is created, False if an existing one is saved.
        **kwargs: Additional keyword arguments.
    '''
    if not created and instance.is_active:     
        from accounts.models import UsersNextActivity   
        creator = instance.created_by
        subject = f'{instance.name_and_standared} has been assigned as your service!'
        message = 'Hello {},\n\nThis is to let you know that the requested service "{}" has been assigned to your service list as it has been tried to add to your service list at a time! If it was not requested by you, you are requested to remove it by visiting your service page!\n\nBest regards,\nAdmin Team'.format(creator.username, instance.name_and_standared)
        una = UsersNextActivity.objects.filter(user = creator).values_list('next_activity', flat=True)
        if instance not in una:
            UsersNextActivity.objects.create(user = creator, next_activity = instance)            
        
        email_recipent = [creator.email] 
        same_tried_by = instance.same_tried_by
        if same_tried_by:
            same_tried_by_json = json.loads(same_tried_by)   
            tried_users_ids = list(same_tried_by_json['users'])
            
            for user_id in tried_users_ids:
                try:
                    tried_user = User.objects.get(id = int(user_id))
                    tuna = UsersNextActivity.objects.filter(user = tried_user).values_list('next_activity', flat=True)
                    if tried_user != creator and instance not in tuna:
                        UsersNextActivity.objects.create(user = tried_user, next_activity = instance)
                        email_recipent.append(tried_user.email)                        
                except:
                    pass
        # Sending mail with one connection    
        send_all_email = [(subject, message, settings.DEFAULT_FROM_EMAIL, [e]) for e in email_recipent]
        send_mass_mail((send_all_email), fail_silently=False) 
                    
        
                
                

                
