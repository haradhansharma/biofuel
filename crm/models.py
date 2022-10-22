from django.db import models
from django_countries.fields import CountryField
import random
from blog.models import *

def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

class Lead(models.Model):
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
    def lead_in_que(self):
        queue = MailQueue.objects.filter(processed = False)
        q_emails = [q.to for q in queue]
        if self.email_address in q_emails:
            return True
        else:
            return False
    
class MailQueue(models.Model):
    to = models.CharField(max_length=256, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    process_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    tried=models.IntegerField(default=0)
    
    def __str__(self):
        return self.to

# The mail ques will be executed by crontab and will e created during saving BlogPost   
class BlogMailQueue(models.Model):
    to = models.CharField(max_length=256, null=True, blank=True)
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)    
    added_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    process_time = models.DateTimeField(auto_now=True)
    tried=models.IntegerField(default=0)
    
    def __str__(self):
        return self.to
