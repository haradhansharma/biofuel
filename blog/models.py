import random
import string
from django.utils import timezone
from django.conf import settings
from django.db import models
from django.urls import reverse
from taggit_autosuggest.managers import TaggableManager
from django.template.defaultfilters import slugify
from django.db.models import Count
from ipware import get_client_ip
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


# Model to track different actions on various objects
class Action(models.Model):
    VIEW = 'view'
    LIKE = 'like'
    ACTION_TYPES = (
        (VIEW, 'View'),
        (LIKE, 'Like')
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_index=True)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')   
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    action_type = models.CharField(max_length=4, choices=ACTION_TYPES, default=VIEW, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)  
    
    class Meta:
        unique_together = ('content_type', 'object_id', 'user', 'action_type')

# Model representing a blog post
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
    
    # Published date for the post
    publish = models.DateTimeField(default=timezone.now, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)    
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')
    
    # Tags associated with the post    
    tags = TaggableManager() 
    
    # GenericRelation to track actions on this post
    actions = GenericRelation(Action)
    
    # Default manager and a custom manager for published posts
    objects = models.Manager()    
    published = PublishedManager()
    
    class Meta:
        ordering = ('-publish',)    
             
    def __str__(self) -> str:
        return self.title   
        
    def save(self, *args, **kwargs):
        
        """
        Custom save method to generate a unique slug for the post.
        """
        
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while BlogPost.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
        
    
    def get_absolute_url(self):
        """
        Get the absolute URL of the blog post for reverse lookup.
        """
        return reverse('blog:post_detail', args=[self.slug])
    
    def view(self, request):
        """
        Record a view action on the blog post.
        """
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
        """
        Calculate and return the total number of views on the blog post.
        """
        return self.actions.filter(action_type=Action.VIEW).count()
    
