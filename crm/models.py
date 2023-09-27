from django.db import models
from django_countries.fields import CountryField
import random
from blog.models import *

from evaluation.models import Evaluator

# Function to generate random 12-digit numbers
def random_digits(): 
    return "%0.12d" % random.randint(0, 999999999999)

class Lead(models.Model):
    """
    Model representing leads in the CRM app.

    This model stores information about leads, including their name, email address, phone number,
    address, city, country, subscription status, and confirmation code.
    """
    lead = models.CharField(max_length=256)
    email_address = models.EmailField(unique=True)
    phone = models.CharField(max_length=256, null=True, blank=True)
    address_1 = models.CharField(max_length=256, null=True, blank=True)
    address_2 = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)
    country = CountryField(blank_label='(select country)', null=True, blank=True)
    subscribed = models.BooleanField(default=True)
    confirm_code = models.CharField(max_length=50, default=random_digits())
    
    def __str__(self):
        return self.lead
    
    @property
    def user(self):
        from accounts.models import User
        user = User.objects.filter(email = self.email_address)
        if user.exists():
            return user.first()
        else:
            return None
    
    @property
    def ns(self):
        from accounts.models import NotificationSettings
        if self.user:
            if not hasattr(self.user, 'notificationsettings'):
                NotificationSettings.objects.create(user=self.user)  
            return self.user.notificationsettings
        return None
        
    
    @property
    def lead_in_que(self):
        """
        Check if the lead's email address is in the mail queue.

        This property checks if the lead's email address is present in the MailQueue's 'to' field.
        Returns True if the email address is in the queue, otherwise returns False.
        """
        queue = MailQueue.objects.filter(processed = False)
        q_emails = [q.to for q in queue]
        if self.email_address in q_emails:
            return True
        else:
            return False
    
class MailQueue(models.Model):
    """
    Model representing queued emails in the CRM app.

    This model stores information about emails in the queue, including the recipient email address,
    when it was added, whether it has been processed, the process time, and the number of times
    it has been tried.
    """
    to = models.CharField(max_length=256, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    process_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    tried=models.IntegerField(default=0)
    
    def __str__(self):
        return self.to

 
class BlogMailQueue(models.Model):
    """
    Model representing queued blog-related emails in the CRM app.

    This model stores information about emails related to blog posts in the queue. It includes the
    recipient email address, the associated blog post, when it was added, whether it has been
    processed, the process time, and the number of times it has been tried.
    """
    to = models.CharField(max_length=256, null=True, blank=True)
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)    
    added_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    process_time = models.DateTimeField(auto_now=True)
    tried=models.IntegerField(default=0)
    
    def __str__(self):
        return self.to
    
class ConsumerMailQueue(models.Model):
    to = models.CharField(max_length=256, null=True, blank=True)
    report = models.ForeignKey(Evaluator, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    process_time = models.DateTimeField(auto_now=True)
    tried=models.IntegerField(default=0)
    
    def __str__(self):
        return self.to
    
