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
from django.utils.safestring import mark_safe
from evaluation.models import ReportMailQueue
from evaluation.helper import clear_evaluator
from django.core.mail.message import EmailMessage
from django.db.models import Count, Q 

import logging
log =  logging.getLogger('log')


def last_process_time():
    """
    Retrieve the time of the most recent email processing.
    
    Returns:
        datetime or None: The datetime of the most recent email processing,
                         or None if no emails have been processed.
    """
    # Retrieve the most recent processed email from the queue
    pendings = MailQueue.objects.filter(process_time__isnull=False).order_by('-process_time').first()
    
    if pendings:
        return pendings.process_time
    return None    


def total_mail_sent():
    """
    Count the total number of emails that have been processed.
    
    Returns:
        int: The total number of processed emails.
    """
    # Count the number of processed emails in the queue
    return MailQueue.objects.filter(processed=True).count()


def pending_queue_count():
    """
    Count the number of emails pending in the queue.
    
    Returns:
        int: The number of pending emails in the queue.
    """
    # Count the number of pending (not yet processed) emails in the queue
    return MailQueue.objects.filter(processed=False).count()


    
def send_custom_mass_mail(
    datatuple, 
    fail_silently=False, 
    auth_user=None,
    auth_password=None, 
    connection=None
    ):
    
    """
    Sends a batch of custom HTML emails using the provided data.

    This function takes a list of email data tuples, each containing information
    about the subject, message, sender, and recipient. It creates EmailMessage
    instances for each tuple, configures them with the provided connection or
    a new one, and sends them in bulk.

    Args:
        datatuple (list of tuples): A list of tuples where each tuple contains:
            - subject (str): The subject of the email.
            - message (str): The HTML content of the email.
            - sender (str): The email address of the sender.
            - recipient (str): The email address of the recipient.
        fail_silently (bool, optional): If False, exceptions during sending
            will be raised. If True, exceptions will be suppressed.
            Defaults to False.
        auth_user (str, optional): The username to use for authentication
            with the email server. Defaults to None.
        auth_password (str, optional): The password to use for authentication
            with the email server. Defaults to None.
        connection (EmailBackend, optional): An existing email connection to
            use for sending emails. If not provided, a new connection will be
            created based on the authentication credentials.
    
    Returns:
        int: The number of successfully sent emails.
    """
    # If connection is not provided, create a new one using the authentication credentials
    connection = connection or get_connection(
        username=auth_user,
        password=auth_password,
        fail_silently=fail_silently,
    )
    # Set the content subtype of the email messages to HTML
    EmailMessage.content_subtype = 'html'
    
    # Create EmailMessage instances for each tuple and store them in a list
    messages = [
        EmailMessage(subject, message, sender, recipient, connection=connection)
        for subject, message, sender, recipient in datatuple
    ]
    
    # Send the list of messages using the provided connection
    return connection.send_messages(messages)    


def send_lead_mail():    
    """
    Sends lead emails from the queue.
    
    This function processes pending lead emails in the MailQueue. It sends an email to each lead with a
    customized message, updates the queue accordingly, and performs cleanup for old or problematic emails.
    
    Returns:
        int: The total number of lead emails sent.
    """
 
    
    # Get the pending emails from the queue
    pendings = MailQueue.objects.filter(processed = False).order_by('-added_at')[:settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME] 
    
    # Get the current site's domain
    current_site = Site.objects.get_current()   
    subject = current_site.domain + ' miss you!'      
     
    mail_to_lead = []    
    deleted_queue_ids = []
    
    for pending in pendings:
        try:
            # Find the corresponding lead         
            lead = Lead.objects.filter(email_address=pending.to).first()  
            
            if lead:    
                # Render the email content using a template         
                message = render_to_string('emails/crm_initial_mail.html', {
                            'confirm_code': lead.confirm_code,
                            'lead' : lead,                                                               
                            'domain': current_site.domain,            
                            }) 
                mail_to_lead.append((subject, mark_safe(message), settings.DEFAULT_FROM_EMAIL, [pending.to]))                            
                
                # Update pending email
                pending.tried += 1       
                pending.processed = True
                pending.process_time = timezone.now()
                pending.save()
                
                # Delete if tried more than 2 times
                if pending.tried > 2:
                    deleted_queue_ids.append(pending.id)
            else:
                pending.delete()  # Delete if corresponding lead not found
                
        except Exception as e:
            log.info(f'There was a problem while creating bulk mail variable due to {e}')

            
    total_sent = len(mail_to_lead)  
    
    # Send emails in bulk
    send_custom_mass_mail((mail_to_lead), fail_silently=False) 
    
    # Delete queued emails with more than 2 tries or older than 90 days
    try:
        MailQueue.objects.filter(id__in=deleted_queue_ids).delete()
        MailQueue.objects.filter(tried__gt=2).delete()
        MailQueue.objects.filter(process_time__lt=timezone.now() - timezone.timedelta(days=90)).delete()
    except Exception as e:
        log.exception(f'There was a problem during deleting the queue: {e}')

    return total_sent


def send_blog_mail():
    """
    Sends blog-related emails from the queue.
    
    This function processes pending blog-related emails in the BlogMailQueue. It sends an email to each recipient
    with personalized content based on the associated blog post and handles cleanup for old or problematic emails.
    
    Returns:
        int: The total number of blog-related emails sent.
    """
    
    
    # Get the pending emails from the queue
    pendings = BlogMailQueue.objects.filter(processed = False).order_by('-added_at')[:settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME] 
    
    # Get the current site's information  
    current_site = site_info()
    subject = 'New post published on "' + current_site.get('domain') + '"!' 
          
    mail_to_lead = []
    deleted_queue_ids = []
        
    for pending in pendings: 
        try:
            # Find the corresponding lead   
            lead = Lead.objects.filter(email_address=pending.to).first()
            
            if lead:
                # Render the email content using a template   
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
                
                # Update pending email
                pending.tried += 1       
                pending.processed = True
                pending.process_time = timezone.now()
                pending.save()
                
                # Delete if tried more than 2 times
                if pending.tried > 2:
                    deleted_queue_ids.append(pending.id)
            else:
                pending.delete()  # Delete if corresponding lead not found
                
        except Exception as e:
            log.info(f'There was a problem while creating bulk mail variabledue to {e}')
    
    total_sent = len(mail_to_lead)  
     
    # Send emails in bulk 
    send_custom_mass_mail((mail_to_lead), fail_silently=False)    
    
    # Delete queued emails with more than 2 tries or older than 90 days
    try:
        BlogMailQueue.objects.filter(id__in=deleted_queue_ids).delete()
        BlogMailQueue.objects.filter(tried__gt=2).delete()
        BlogMailQueue.objects.filter(process_time__lt=timezone.now() - timezone.timedelta(days=90)).delete()
    except Exception as e:
        log.exception(f'There was a problem during deleting the queue: {e}')
    
    
    return total_sent



def send_report_queue():
    
    """
    Sends report-related emails from the queue.
    
    This function processes pending report-related emails in the ReportMailQueue. It sends an email to each recipient
    with personalized content based on the associated report update and handles cleanup for old or problematic emails.
    
    Returns:
        int: The total number of report-related emails sent.
    """
    
    # Get the pending emails from the queue
    pendings = ReportMailQueue.objects.filter(processed = False).order_by('-added_at')[:settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME] 
    
    # Count the number of pending emails
    batch = pendings.count()  
    
    # Get the current site's information
    current_site = site_info()  
    
    # Prepare the subject for the email
    subject = f'Report has been updated at "{current_site.get("domain")}"!'
    
    mail_to_lead = []    
    deleted_queue_ids = []
    
    for pending in pendings: 
        try:
            # Render the email content using a template     
            message = render_to_string('emails/feedback_update.html', {                        
                        'pending' : pending,                                                               
                        'current_site': current_site,                               
                        }) 
            mail_to_lead.append((subject, mark_safe(message), settings.DEFAULT_FROM_EMAIL, [pending.to]))                            
            
            # Update pending email
            pending.tried += 1       
            pending.processed = True
            pending.process_time = timezone.now()
            pending.save()
            
            # Delete if tried more than 2 times
            if pending.tried > 2:
                deleted_queue_ids.append(pending.id)
                
        except Exception as e:
            log.info(f'There was a problem while creating bulk mail variable due to {e}')
    
    total_sent = len(mail_to_lead)  
      
    # Send emails in bulk
    send_custom_mass_mail((mail_to_lead), fail_silently=False)
    
    # Delete queued emails with more than 2 tries or older than 90 days
    try:
        ReportMailQueue.objects.filter(id__in=deleted_queue_ids).delete()
        ReportMailQueue.objects.filter(tried__gt=2).delete()
        ReportMailQueue.objects.filter(process_time__lt=timezone.now() - timezone.timedelta(days=90)).delete()
    except Exception as e:
        log.exception(f'There was a problem during deleting the queue: {e}')

    
    return total_sent 


class SendQueueMail(CronJobBase):    
    """
    A cron job to send various types of queued mails in bulk.
    
    This cron job is responsible for sending different types of queued mails, including lead mails,
    blog mails, and report mails, in bulk at scheduled intervals.
    """    
    RUN_EVERY_MINS = 5
    RETRY_AFTER_FAILURE_MINS = 1
    MIN_NUM_FAILURES = 2    
    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'crm.send_queue_mail'   
    
    def do(self):  
        """
        Executes the cron job to send queued mails in bulk.
        
        This method triggers the sending of queued mails for different types (leads, blogs, reports)
        in bulk using respective functions. It logs the number of mails sent for each type.
        """
        try:
            # Send lead mails
            total_lead_mails_sent = send_lead_mail()
            log.info(f'{total_lead_mails_sent} lead mail(s) have been sent')
            
            # Send blog mails
            total_blog_mails_sent = send_blog_mail()
            log.info(f'{total_blog_mails_sent} blog mail(s) have been sent')
            
            # Send report mails
            total_report_mails_sent = send_report_queue()
            log.info(f'{total_report_mails_sent} report mail(s) have been sent')
        
        except Exception as e:
            log.exception(f'An error occurred while sending queued mails: {e}')
   

class DeleteIncompleteReports(CronJobBase):
    """
    A cron job to delete incomplete reports.
    
    This cron job periodically deletes incomplete reports from the system using the `clear_evaluator` function.
    """    
    RUN_EVERY_MINS = 5
    RETRY_AFTER_FAILURE_MINS = 1
    MIN_NUM_FAILURES = 2    
    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'crm.delete_incomplete_reports'   
    
    def do(self):      
        """
        Executes the cron job to delete incomplete reports.
        
        This method triggers the `clear_evaluator` function to remove incomplete reports from the system.
        It logs the number of incomplete reports that have been deleted.
        """ 
        try:
            deleted_count = clear_evaluator()
            log.info(f'{deleted_count} incomplete report(s) have been deleted')
        except Exception as e:
            log.exception(f'An error occurred while deleting incomplete reports: {e}')

     
        
        
        
            

