from time import process_time
from doc.doc_processor import site_info

from doc.models import ExSite
from .models import BlogMailQueue, MailQueue, Lead
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail, get_connection
from django.utils import timezone 
from django_cron import CronJobBase, Schedule
from blog.models import *
from concurrent.futures import ProcessPoolExecutor, as_completed, ThreadPoolExecutor
import django
from django.utils.safestring import mark_safe
from evaluation.models import ReportMailQueue
from evaluation.helper import clear_evaluator
from django.core.mail.message import EmailMessage
from django.db.models import Count, Q 

import logging
log =  logging.getLogger('log')

CURRENT = timezone.now()

def last_process_time():    
    pendings = MailQueue.objects.all().order_by('-process_time').first()        
    return pendings.process_time 
    
def total_mail_sent():    
    return  MailQueue.objects.filter(processed = True).count()       
    

def pending_queue_count():
    try:        
        return MailQueue.objects.filter(processed = False).count()
    except:
        return 0   


    
def send_custom_mass_mail(datatuple, fail_silently=False, auth_user=None,
                   auth_password=None, connection=None):
    """
    coloned fromt he core
    """
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    EmailMessage.content_subtype = 'html'
    messages = [
        EmailMessage(subject, message, sender, recipient, connection=connection)
        for subject, message, sender, recipient in datatuple
    ]
    return connection.send_messages(messages)
    
    

def send_lead_mail():    
    # 1. It checks if the last time the function was called is more than EXECUT_MAIL_IN_SECONDS seconds ago.
    # 2. If it is, it gets LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME number of emails from the MailQueue table that haven't been processed yet.
    # 3. It then loops through each email and sends an email to each one.
    # 4. If the email has been tried more than 2 times, it deletes it from the MailQueue table.
    # 5. if process time more then 90 days that record will be deleted
    queued = MailQueue.objects.all().order_by('-added_at')   
    pendings = queued.filter(processed = False)[:settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME] 
    # batch = pendings.count()  
    current_site = Site.objects.get_current()   
    subject = current_site.domain + ' miss you!'       
    mail_to_lead = []    
    for pending in pendings:
        try:
            lead = Lead.objects.filter(email_address = pending.to)[0]     
            message = render_to_string('emails/crm_initial_mail.html', {
                        'confirm_code': lead.confirm_code,
                        'lead' : lead,                                                               
                        'domain': current_site.domain,            
                        }) 
            mail_to_lead.append((subject, mark_safe(message), settings.DEFAULT_FROM_EMAIL, [pending.to]))                            
            # pending_to_this = queued.filter(to = pending.to, processed = False)[0]
            pending.tried += 1       
            pending.processed = True
            pending.process_time = CURRENT
            pending.save()
        except Exception as e:
            log.info(f'There was a problem while creating bulk mail variabledue to {e}')

            
    total_sent = len(mail_to_lead)    
    #send bulk mail using only one conenction
    #log.info(f'Initializing CRM bulk mail sending operation for total {total_sent} mail !')
    send_custom_mass_mail((mail_to_lead), fail_silently=False)
    #log.info(f'{total_sent} mail sent out of pending {batch} ')
    try:  
        #log.info('Deleting all leads from queue which were failed on 2nd time attemnpt to send mail! ')  
        queued.filter(tried__gt = 2).delete()    
        #log.info('Deleting blog queue which are older then 90 days') 
        queued.filter(process_time__gt = (CURRENT + timezone.timedelta(days = 90))).delete()  
        #log.info('Delete Queue older then 90 days')
    except Exception as e:
        log.info(f'There was a problem during deleting the queue {e}')

    
    return total_sent

def send_blog_mail():
    # 1. It checks if the last time the function was called is more than EXECUT_MAIL_IN_SECONDS seconds ago.
    # 2. If it is, it gets LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME number of emails from the MailQueue table that haven't been processed yet.
    # 3. It then loops through each email and sends an email to each one.
    # 4. If the email has been tried more than 2 times, it deletes it from the MailQueue table.
    # 5. if process time more then 90 days that record will be deleted
    queued = BlogMailQueue.objects.all().order_by('-added_at')
    pendings = queued.filter(processed = False)[:settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME] 
    # batch = pendings.count()  
    current_site = site_info()
    subject = 'New post published on "' + current_site.get('domain') + '"!'       
    mail_to_lead = []    
    for pending in pendings: 
        try:
            lead = Lead.objects.filter(email_address = pending.to)[0]    
            post_tags_id = pending.blog.tags.values_list('id', flat=True)
            similar_posts = BlogPost.published.filter(tags__in = post_tags_id).exclude(id=pending.blog.id)
            similar_posts = similar_posts.annotate(same_tags = Count('tags')).order_by('-same_tags', '-publish')[:2]   
            message = render_to_string('emails/crm_blog_mail.html', {                        
                        'lead' : lead,                                                               
                        'current_site': current_site,   
                        'blog': pending.blog,
                        'similar_posts' : similar_posts       
                        }) 
            message.content_subtype = "html"
            mail_to_lead.append((subject, message, settings.DEFAULT_FROM_EMAIL, [pending.to]))                            
            # pending_to_this = queued.filter(to = pending.to, processed = False)[0]
            pending.tried += 1       
            pending.processed = True
            pending.process_time = CURRENT
            pending.save()
        except Exception as e:
            log.info(f'There was a problem while creating bulk mail variabledue to {e}')
    
    total_sent = len(mail_to_lead)    
    #send bulk mail using only one conenction
    #log.info(f'Initializing CRM blog bulk mail sending operation for total {total_sent} mail!')
    send_custom_mass_mail((mail_to_lead), fail_silently=False)
    
    #log.info(f'{total_sent} blog mail sent out of pending {batch} ')
    
    try:  
        #log.info('Deleting all blogs leads from queue which were failed on 2nd time attemnpt to send mail! ')  
        queued.filter(tried__gt = 2).delete()      
        #log.info('Deleting blog queue which are older then 90 days')
        queued.filter(process_time__gt = (CURRENT + timezone.timedelta(days = 90))).delete()   
        #log.info('Delete Queue older then 90 days')
         
    except Exception as e:
        log.info(f'There was a problem during deleting the queue {e}')

    
    return total_sent

def send_report_queue():
    queued = ReportMailQueue.objects.all().order_by('-added_at')
    pendings = queued.filter(processed = False)[:settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME] 
    batch = pendings.count()  
    current_site = site_info()
    try:
        subject = 'Report has been updated at "' + current_site.get('domain') + '"!'         
    except Exception as e:
        pass
    mail_to_lead = []    
    for pending in pendings: 
        try:
            # lead = Lead.objects.filter(email_address = pending.to)[0]      
            message = render_to_string('emails/feedback_update.html', {                        
                        'pending' : pending,                                                               
                        'current_site': current_site,                               
                        }) 
            mail_to_lead.append((subject, mark_safe(message), settings.DEFAULT_FROM_EMAIL, [pending.to]))                            
            # pending_to_this = queued.filter(to = pending.to, processed = False)[0]
            pending.tried += 1       
            pending.processed = True
            pending.process_time = CURRENT
            pending.save()
        except Exception as e:
            log.info(f'There was a problem while creating bulk mail variable due to {e}')
    
    total_sent = len(mail_to_lead)    
    #send bulk mail using only one conenction
    # log.info(f'Initializing CRM blog bulk mail sending operation for total {total_sent} mail!')
    send_custom_mass_mail((mail_to_lead), fail_silently=False)
    
    # log.info(f'{total_sent} blog mail sent out of pending {batch} ')
    
    try:  
        #log.info('Deleting all blogs leads from queue which were failed on 2nd time attemnpt to send mail! ')  
        queued.filter(tried__gt = 2).delete()      
        #log.info('Deleting blog queue which are older then 90 days')
        queued.filter(process_time__gt = (CURRENT + timezone.timedelta(days = 90))).delete()   
        #log.info('Delete Queue older then 90 days')
         
    except Exception as e:
        log.info(f'There was a problem during deleting the queue {e}')

    
    return total_sent
    
    
    
    
    




# crontab codein linux
# */5 * * * * source /home/krishnahara/.bashrc && source /home/krishnahara/env/bin/activate && python /home/krishnahara/project-root/manage.py runcrons > /home/ubuntu/project-root/cronjob.log   
# source virtualenvwrapper.sh && workon env && python /home/krishnahara/biofuel/manage.py runcrons
# /home/krishnahara/env/bin/python3.9   /home/krishnahara/biofuel/manage.py  runcrons
class SendQueueMail(CronJobBase):
    log.info('Initializing CRONJOB to send bulk mail, blog mail and report mail!!')
    RUN_EVERY_MINS = 1
    RETRY_AFTER_FAILURE_MINS = 1
    MIN_NUM_FAILURES = 2    
    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'crm.send_queue_mail'   
    
    def do(self):        
        log.info(f'{send_lead_mail()} lead mail has been sent') 
        log.info(f'{send_blog_mail()} blog mail has been sent') 
        log.info(f'{send_report_queue()} report mail has been sent') 
        
        
        
# crontab codein linux
# */5 * * * * source /home/ubuntu/.bashrc && source /home/ubuntu/env/bin/activate && python /home/ubuntu/project-root/manage.py runcrons > /home/ubuntu/project-root/cronjob.log   
class DeleteIncompleteReports(CronJobBase):
    log.info('Initializing CRONJOB to delete incomplete report!!')
    RUN_EVERY_MINS = 1
    RETRY_AFTER_FAILURE_MINS = 1
    MIN_NUM_FAILURES = 2    
    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'crm.delete_incomplete_reports'   
    
    def do(self):       
        log.info(f'{clear_evaluator()} Incomplete report has been deleted') 
        
        
        
        
            

