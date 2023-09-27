from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from crm.models import *
import logging
log =  logging.getLogger('log')


# Signal handler to create or update BlogMailQueue entries when a BlogPost is saved
@receiver(post_save, sender=BlogPost)
def send_to_mail_que(sender, instance, created, **kwargs):
    """
    Signal handler to create or update BlogMailQueue entries when a BlogPost is saved.

    If a new BlogPost is created and its status is 'published', a BlogMailQueue entry
    will be created for each subscribed lead.

    If a BlogPost is updated, and its status is changed to 'draft', any unprocessed
    BlogMailQueue entries related to that post will be deleted. If the status is changed
    to 'published' and there are no existing BlogMailQueue entries, new entries will be
    created for each subscribed lead.

    :param sender: The sender of the signal.
    :param instance: The instance of the BlogPost that was saved.
    :param created: Boolean indicating if the instance was newly created.
    """
    
    log.info(f'Initializing BlogMailQueue for Blog {instance.title} to notify to the subscribed leads  ')
    
    leads = Lead.objects.filter(subscribed = True)    
    
    if created:
        log.info(f'New Blog titled {instance.title} detected')
        if instance.status == 'published':
            queued = 1
            for lead in leads:
                if lead.ns.blog_notifications:
                    BlogMailQueue.objects.create(to=lead.email_address, blog = instance)
                    queued += 1
            log.info(f'Total {queued} BlogMailQueue created for new created blog {instance.title} ')
    else:  
        log.info(f'A blog titled {instance.title} has been updated')      
        if instance.status == 'draft':            
            queues = BlogMailQueue.objects.filter(blog = instance, processed = False)
            for queue in queues:
                queue.delete()
            log.info(f'BlogMailQueue has been deleted for {instance.title} as the blog status has been changed to "Draft"!')
        if instance.status == 'published':            
            queues = BlogMailQueue.objects.filter(blog = instance)
            if not queues.exists():
                queued = 1
                for lead in leads:
                    if lead.ns.blog_notifications:
                        BlogMailQueue.objects.create(to=lead.email_address, blog = instance)
                        queued += 1
                    
                log.info(f'Total {queued} BlogMailQueue created for updated blog {instance.title} ')
    log.info(f'BlogMailQueue completing for the blog titled {instance.title} ')
                
            
# Signal handler to delete BlogMailQueue entries when a BlogPost is deleted        
@receiver(post_delete, sender=BlogPost)
def delete_mail_queues(sender, instance, **kwargs):   
    """
    Signal handler to delete BlogMailQueue entries when a BlogPost is deleted.

    If there are unprocessed BlogMailQueue entries related to the deleted BlogPost,
    they will be deleted as well.

    :param sender: The sender of the signal.
    :param instance: The instance of the BlogPost that was deleted.
    """ 
    queues = BlogMailQueue.objects.filter(blog = instance, processed = False)
    deleted = 1
    for queue in queues:
        queue.delete()
        deleted += 1
    log.info(f'{deleted} BlogMailQueue has been deleted as blog titled {instance.title} has been deleted ')
        
    
