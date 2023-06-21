import random
import string
from django.utils import timezone
from django.conf import settings
from django.db import models
# from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
# from taggit.managers import TaggableManager
from taggit_autosuggest.managers import TaggableManager
from django.template.defaultfilters import slugify
from django.db.models import Count
from ipware import get_client_ip
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Action(models.Model):
    VIEW = 'view'
    LIKE = 'like'
    ACTION_TYPES = (
        (VIEW, 'View'),
        (LIKE, 'Like')
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,db_index=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')   
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    action_type = models.CharField(max_length=4, choices=ACTION_TYPES, default=VIEW,db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)  


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class BlogPost(models.Model):
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=252)
    image = models.ImageField(upload_to='featured_image/') 
    slug = models.SlugField(null=True, blank=True, editable=False, max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts', editable=False)
    body = models.TextField()
    
    publish = models.DateTimeField(default=timezone.now, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')    
    tags = TaggableManager() 
    actions = GenericRelation(Action)
    
    
    
    
    objects = models.Manager()
    published = PublishedManager()
    
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
    
    def view(self, request):
        client_ip, is_routable = get_client_ip(request)
        Action.objects.create(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
            user=request.user if request.user.is_authenticated else None,
            ip_address=client_ip,
            action_type=Action.VIEW
        ) 
    @property
    def total_view(self): 
        total = Action.objects.filter(
            content_type=ContentType.objects.get_for_model(self),
            object_id=self.pk,
            action_type=Action.VIEW
        ).count()
        return total
    
