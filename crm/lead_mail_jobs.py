from time import process_time
from doc.doc_processor import site_info
from doc.models import ExSite
from .models import BlogMailQueue, MailQueue, Lead, ConsumerMailQueue
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
from evaluation.helper import build_full_url

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
    pendings = MailQueue.objects.filter(processed = False).order_by('added_at')[:settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME] 
    
    # Get the current site's domain
    current_site = Site.objects.get_current()   
    subject = current_site.domain + ' miss you!'      
     
    mail_to_lead = []    
    deleted_queue_ids = []
    updated_pendings = []
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
                updated_pendings.append(pending)
                
                # Delete if tried more than 2 times
                if pending.tried > 2:
                    deleted_queue_ids.append(pending.id)
            else:
                pending.delete()  # Delete if corresponding lead not found
                
        except Exception as e:
            log.info(f'There was a problem while creating bulk mail variable due to {e}')

            
    total_sent = len(mail_to_lead)  
    
    MailQueue.objects.bulk_update(updated_pendings, fields=['tried', 'processed', 'process_time']) 
    
    # Send emails in bulk
    send_custom_mass_mail((mail_to_lead), fail_silently=False) 
    
    # Delete queued emails with more than 2 tries or older than 90 days
    try:
        cutoff_date = timezone.now() - timezone.timedelta(days=90)
        combined_query = Q(id__in=deleted_queue_ids) | Q(tried__gt=2) | Q(process_time__lt=cutoff_date)
        MailQueue.objects.filter(combined_query).delete()  
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
    pendings = BlogMailQueue.objects.filter(processed = False).order_by('added_at')[:settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME] 
    
    # Get the current site's information  
    current_site = site_info()
    subject = 'New post published on "' + current_site.get('domain') + '"!' 
          
    mail_to_lead = []
    deleted_queue_ids = []
    updated_pendings = []
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
                updated_pendings.append(pending)
                
                # Delete if tried more than 2 times
                if pending.tried > 2:
                    deleted_queue_ids.append(pending.id)
            else:
                pending.delete()  # Delete if corresponding lead not found
                
        except Exception as e:
            log.info(f'There was a problem while creating bulk mail variabledue to {e}')
    
    total_sent = len(mail_to_lead)  
    
    BlogMailQueue.objects.bulk_update(updated_pendings, fields=['tried', 'processed', 'process_time']) 
     
    # Send emails in bulk 
    send_custom_mass_mail((mail_to_lead), fail_silently=False)    
    
    # Delete queued emails with more than 2 tries or older than 90 days
    try:
        cutoff_date = timezone.now() - timezone.timedelta(days=90)
        combined_query = Q(id__in=deleted_queue_ids) | Q(tried__gt=2) | Q(process_time__lt=cutoff_date)
        BlogMailQueue.objects.filter(combined_query).delete()  
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
    pendings = ReportMailQueue.objects.filter(processed = False).order_by('added_at')[:settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME] 
    
    # Count the number of pending emails
    batch = pendings.count()  
    
    # Get the current site's information
    current_site = site_info()  
    
    # Prepare the subject for the email
    subject = f'Report has been updated at "{current_site.get("domain")}"!'
    
    mail_to_lead = []    
    deleted_queue_ids = []
    updated_pendings = []
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
            updated_pendings.append(pending)
            
            # Delete if tried more than 2 times
            if pending.tried > 2:
                deleted_queue_ids.append(pending.id)
                
        except Exception as e:
            log.info(f'There was a problem while creating bulk mail variable due to {e}')
    
    total_sent = len(mail_to_lead)  
    ReportMailQueue.objects.bulk_update(updated_pendings, fields=['tried', 'processed', 'process_time']) 
    
    # Send emails in bulk
    send_custom_mass_mail((mail_to_lead), fail_silently=False)
    
    # Delete queued emails with more than 2 tries or older than 90 days
    try:
        cutoff_date = timezone.now() - timezone.timedelta(days=90)
        combined_query = Q(id__in=deleted_queue_ids) | Q(tried__gt=2) | Q(process_time__lt=cutoff_date)
        ReportMailQueue.objects.filter(combined_query).delete()    
    except Exception as e:
        log.exception(f'There was a problem during deleting the queue: {e}')

    
    return total_sent 


def send_new_report_notification():  
    
    """
    Send notifications for new fuel reports to consumers.

    This function retrieves pending email notifications from the queue,
    constructs notification messages, and sends them to consumers. It also
    handles updating the queue and deleting old queue entries.

    Returns:
        int: The total number of notifications sent.
    """ 
    
    # Get the pending emails from the queue
    pendings = ConsumerMailQueue.objects.filter(processed = False).order_by('added_at')[:settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME] 
    
    # Get the current site's information
    current_site = site_info()
    from_email = settings.DEFAULT_FROM_EMAIL
    
    subject = 'New Fuel Submitted on "' + current_site.get('domain').upper() + '"!' 
          
    mail_to_send = []
    deleted_queue_ids = []
    updated_pendings = []
    
    try:
        
        for pending in pendings:    
            # Construct the notification message
            message = f"Dear {pending.to.upper()}, \n\n"
            message += f"New fuel has been submitted or updated. You may learn more about the fuel by visiting the link below. \n\n"
            message += f"{build_full_url(pending.report.get_absolute_url())} \n\n"
            message += f"We believe this information will be valuable for your daily business operations. \n\n"
            message += f"If you wish to stop receiving this notification, please adjust your account settings accordingly. \n\n"
            message += f"Best Regards \n\n"
            message += f"GFVP TEAM"
            
            mail_to_send.append((subject, message, from_email, [pending.to]))
            
            pending.tried += 1
            pending.processed = True
            pending.process_time = timezone.now()
            updated_pendings.append(pending)
            
            if pending.tried > 2:
                deleted_queue_ids.append(pending.id)        
                
        # Update the pending records in bulk     
        ConsumerMailQueue.objects.bulk_update(updated_pendings, fields=['tried', 'processed', 'process_time'])
        
        # Send the notification emails
        total_sent = len(mail_to_send)         
        send_custom_mass_mail((mail_to_send), fail_silently=False)       

        # Calculate the cutoff date for deleting old queue entries
        cutoff_date = timezone.now() - timezone.timedelta(days=90)
        combined_query = Q(id__in=deleted_queue_ids) | Q(tried__gt=2) | Q(process_time__lt=cutoff_date)
        
        # Delete old queue entries that meet the specified conditions
        ConsumerMailQueue.objects.filter(combined_query).delete()      
    except Exception as e:
        # Handle exceptions and log warnings
        log.warning(f'There was a problem in sending Consumer mail for: {e}')
    
    
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
            
            total_consumer_mail_sent = send_new_report_notification()
            log.info(f'{total_consumer_mail_sent} report mail(s) have been sent')
        
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

     
        
        
        
            

