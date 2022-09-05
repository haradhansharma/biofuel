from .models import MailQueue, Lead
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail 
from django.utils import timezone 
from django_cron import CronJobBase, Schedule

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




def send_lead_mail():   
    # 1. It checks if the last time the function was called is more than EXECUT_MAIL_IN_SECONDS seconds ago.
    # 2. If it is, it gets LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME number of emails from the MailQueue table that haven't been processed yet.
    # 3. It then loops through each email and sends an email to each one.
    # 4. If the email has been tried more than 2 times, it deletes it from the MailQueue table.
    queued = MailQueue.objects.all()     
    pendings = queued.filter(processed = False).order_by('-added_at')[:settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME] 
    batch = pendings.count()  
    current_site = Site.objects.get_current()   
    subject = current_site.domain + ' miss you!'       
    mail_to_lead = []    
    for pending in pendings:
        try:
            lead = Lead.objects.get(email_address = pending.to)       
            message = render_to_string('emails/crm_initial_mail.html', {
                        'confirm_code': lead.confirm_code,
                        'lead' : lead,                                                               
                        'domain': current_site.domain,            
                        }) 
            mail_to_lead.append((subject, message, settings.DEFAULT_FROM_EMAIL, [pending.to]))                            
            pending_to_this = MailQueue.objects.get(to = pending.to, processed = False)
            pending_to_this.tried += 1       
            pending_to_this.processed = True
            pending_to_this.process_time = CURRENT
            pending_to_this.save()
        except:
            pass
    #send bulk mail using only one conenction
    log.info('Initializing CRM bulk mail sending operation!')
    send_mass_mail((mail_to_lead), fail_silently=False)
    log.info(f'{len(mail_to_lead)} mail sent out of pending {batch} ')
    try:  
        log.info('Deleting all leads from queue which were failed on 2nd time attemnpt to send mail! ')  
        queued.filter(tried__gt = 2).delete()        
    except:
        pass
    
    return batch



# crontab codein linux
# */5 * * * * source /home/krishnahara/.bashrc && source /home/krishnahara/env/bin/activate && python /home/krishnahara/project-root/manage.py runcrons > /home/ubuntu/project-root/cronjob.log   
# source virtualenvwrapper.sh && workon env && python /home/krishnahara/biofuel/manage.py runcrons
# /home/krishnahara/env/bin/python3.9   /home/krishnahara/biofuel/manage.py  runcrons
class SendQueueMail(CronJobBase):
    log.info('Initializing CRONJOB to send bulk mail from MailQueue Table!!')
    RUN_EVERY_MINS = settings.EXECUT_MAIL_IN_SECONDS/60
    RETRY_AFTER_FAILURE_MINS = 5
    MIN_NUM_FAILURES = 2    
    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'crm.send_queue_mail'   
    
    def do(self):    
        send_lead_mail()

