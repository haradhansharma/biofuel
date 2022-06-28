from django.db import models
from django.apps import apps
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.validators import FileExtensionValidator


class ExSite(models.Model):
    site = models.OneToOneField(Site, primary_key=True, verbose_name='site', on_delete=models.CASCADE)
    site_meta = models.CharField(max_length=256)
    site_description = models.TextField(max_length=500)
    site_meta_tag =models.CharField(max_length=255)
    site_favicon = models.ImageField(upload_to='site_image')
    site_logo = models.ImageField(upload_to='site_image')
    slogan = models.CharField(max_length=150, default='')
    og_image = models.ImageField(upload_to='site_image')
    mask_icon = models.FileField(upload_to='site_image', validators=[FileExtensionValidator(['svg'])])
    
    
    phone = models.CharField(max_length=15)
    email = models.EmailField()    
    location=models.CharField(max_length=120)
    facebook_link = models.URLField()
    twitter_link = models.URLField()
    linkedin_link = models.URLField()
    
    #This is beeing used in the evaluation procedure.
    qualified_ans_range = models.IntegerField(default=1)
    
    # It is implemented for future roadmap
    objects = models.Manager()
    on_site = CurrentSiteManager('site')
    
    def __str__(self):
        return self.site.__str__()  

def apps_choice():
    PROJECT_APPS = [app.verbose_name for app in apps.get_app_configs()]    
    al = []
    for pa in PROJECT_APPS:        
        tc = (            
            slugify(pa) , pa,        )
        al.append(tc)        
    return al

class Acordion(models.Model):
    button_text = models.CharField(max_length=256)
    button_des = models.TextField()
    apps = models.CharField(max_length=50, choices=apps_choice())    
    
    def __str__(self):
        return self.button_text