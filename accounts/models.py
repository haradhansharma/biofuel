from evaluation.models import DifinedLabel
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from crm.models import *
from .helper import CustomsernameValidator
from django.utils.translation import gettext_lazy as _
from django.apps import apps


class UserType(models.Model):
    
    '''
    database modelto handle user type
    The items for this model should be ceated by admin
    minimum one user type is mandatory to work system properly
    '''
    
    # It will display everywhere t identify the usr type.
    name = models.CharField(max_length=252)   
    
    # It is being used as url and creted autometically from name.  
    slug = models.SlugField(unique=True, null=False, blank=False) 
    
    #It is being diplayed as user type identifier(visual)   
    icon = models.ImageField(upload_to = 'usertype/')
    
    # Timestamp when it is created. Required for sitemap it need to create later
    created = models.DateTimeField(auto_now_add=True)
    
    # IF user type representing producer it must be true
    is_producer = models.BooleanField(default=False)
    
    #IF user type representing expert it must be true.
    is_expert = models.BooleanField(default=False)
    
    #IF user type representing consumer it must be true
    is_consumer = models.BooleanField(default=False)  
    
    #IF user type representing consumer it must be true
    is_marine = models.BooleanField(default=False)  
    
    #To control display order it is mandatory  
    sort_order = models.IntegerField(default=1)
    
    #To control display. Curently it is implemented only on front page.
    active = models.BooleanField(default=False)
   
    # Don't change this. as it it dijango's default
    def get_absolute_url(self):        
        return reverse('types', args=[str(self.slug)])

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['sort_order']
        
        # Can be control in admin who can produce or reproduce it.
        permissions = (("can_access_usertype", "Can access usertype"),)
        





class User(AbstractUser):   
    username_validator = CustomsernameValidator() 
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters and numbers only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    '''
    Inheriting Django's default user model with custom fields.
    ''' 
    usertype = models.ForeignKey(UserType, on_delete=models.CASCADE, related_name='user_usertype')   
    email = models.EmailField('E-Mail Address', unique=True)
    phone = models.CharField(max_length=252, null=True, blank=True)
    orgonization = models.CharField(max_length=252, verbose_name='Organization')
    experts_in = models.ForeignKey(DifinedLabel, on_delete=models.SET_NULL, null=True, blank=True, related_name = 'user_label', limit_choices_to={'common_status': False} )  
    term_agree = models.BooleanField(null=False, blank=False,)
    email_verified = models.BooleanField(default=False)
    newsletter_subscription = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True, verbose_name='Profile is Public', help_text='If true profile data visible to logged in other users of the platform.')
    
    
    
    
 
    #don't change this
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        ordering = ['-date_joined']
    

    def __str__(self):
        return self.email
    
    
    # send email after activating account by admin from admin GUI.
    def send_active_mail(self, request):
        from django.template.loader import render_to_string
        from django.contrib.sites.shortcuts import get_current_site
        current_site = get_current_site(request)
        subject = 'Account has been created, you can login now!'      
       
        # and calls its render() method immediately.
        if self.email is not None:
            message = render_to_string('emails/account_activated.html', {
                'user': self,                    
                'domain': current_site.domain,
                'login' : request.build_absolute_uri('login')                 
            })
            self.email_user(subject, '', html_message=message)
            
    @property
    def get_profile(self):
        return self.profile
    
    @property
    def get_type(self):
        try:
            name = self.usertype.name
        except Exception as e:
            name = False            
        return name
    
    @property
    def expert_in_name(self):
        try:
            name = self.experts_in.name
        except Exception as e:
            name = False            
        return name
    
    @property
    def is_producer(self):
        if self.usertype.is_producer:
            return True
        return False    
    
    @property
    def is_expert(self):
        if self.usertype.is_expert:
            return True
        return False
    
    @property
    def is_consumer(self):
        if self.usertype.is_consumer:
            return True
        return False
    
    @property
    def is_marine(self):
        if self.usertype.is_marine:
            return True
        return False
    
    # @property
    # def is_subscriber(self):        
    #     lead = Lead.objects.filter(email_address = self.email)
    #     if lead.exists():            
    #         return True
    #     else:            
    #         return False    
    
    @property
    def is_subscriber(self):
        if hasattr(self, '_is_subscriber'):
            return self._is_subscriber

        lead = Lead.objects.filter(email_address=self.email)
        if lead.exists():
            self._is_subscriber = True
        else:
            self._is_subscriber = False

        return self._is_subscriber
        

    # @property
    # def selected_activities(self):        
    #     if not hasattr(self, '_selected_activities'):
    #         self._selected_activities = self.user_next_activity.all().prefetch_related('next_activity__quotnextactivity__related_questions')
    #     return self._selected_activities
    
    
    @property
    def selected_activities(self):        
        if not hasattr(self, '_selected_activities'):
            self._selected_activities = self.user_next_activity.all().prefetch_related('next_activity__quotnextactivity__related_questions') or False
        return self._selected_activities
    
    def get_absolute_url(self):        
        return reverse('accounts:user_link')
    
    
   
class Profile(models.Model):
    # It is beeing created autometically during signup by using signal.
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company_logo = models.ImageField(upload_to='company_logo', blank=True)
    about = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    established = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return 'Profile for ' +  str(self.user.username)
    
    @property
    def profile_logo(self):        
        return self.company_logo.url if self.company_logo != '' else '/static/rings.png'
    
    
class UsersNextActivity(models.Model):
    from evaluation.models import NextActivities
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_next_activity' 
        )
    next_activity = models.ForeignKey(
        NextActivities, 
        on_delete=models.CASCADE, 
        related_name='next_activities' 
        )
   


