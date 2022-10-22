from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import *
from crm.models import *
import logging
log =  logging.getLogger('log')


# After saving BlogPost
# IF post created new and status is published BlogMailQue will be created for each lead for this post.
# If Post is updated if status is draft then if mail is still in queue having without processed will be deleted
# and if published then mail ques will be created for the updated post
@receiver(post_save, sender=BlogPost)
def send_to_mail_que(sender, instance, created, **kwargs):
    log.info(f'Initializing BlogMailQueue for Blog {instance.title} to notify to the subscribed leads  ')
    leads = Lead.objects.filter(subscribed = True)    
    if created:
        log.info(f'New Blog titled {instance.title} detected')
        if instance.status == 'published':
            queued = 1
            for lead in leads:
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
                    BlogMailQueue.objects.create(to=lead.email_address, blog = instance)
                    queued += 1
                    
                log.info(f'Total {queued} BlogMailQueue created for updated blog {instance.title} ')
    log.info(f'BlogMailQueue completing for the blog titled {instance.title} ')
                
            
# After deleting  BlogPost
# if there is unprocessed queue for this blog post will be deleted           
@receiver(post_delete, sender=BlogPost)
def delete_mail_queues(sender, instance, **kwargs):    
    queues = BlogMailQueue.objects.filter(blog = instance, processed = False)
    deleted = 1
    for queue in queues:
        queue.delete()
        deleted += 1
    log.info(f'{deleted} BlogMailQueue has been deleted as blog titled {instance.title} has been deleted ')
        
    
