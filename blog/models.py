import random
import string
from django.utils import timezone
from django.conf import settings
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
# from taggit.managers import TaggableManager
from taggit_autosuggest.managers import TaggableManager
from django.template.defaultfilters import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class BlogPost(models.Model):
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=252)
    image = models.ImageField(upload_to='featured_image/%Y/%m/%d/') 
    slug = models.SlugField(null=True, blank=True, editable=False, max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts', editable=False)
    body = RichTextUploadingField()
    
    publish = models.DateTimeField(default=timezone.now, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')    
    tags = TaggableManager() 
    
    
    
    objects = models.Manager()#default manager
    published = PublishedManager()#Cutom Manager
    
    
    class Meta:
        ordering = ('-publish',)    
             
    def __str__(self) -> str:
        return self.title  
        
        
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_sample = slugify(self.title)            
            if BlogPost.objects.filter(slug=slug_sample).exists():
                # Generate a random alphanumeric string of length 6
                random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                slug_sample = slugify(self.title + ' ' + random_string)
            self.slug = slug_sample
        super(BlogPost, self).save(*args, **kwargs)
        
    
    
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])
    
    
