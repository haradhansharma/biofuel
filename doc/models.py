from django.db import models
from django.apps import apps
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.validators import FileExtensionValidator


class ExSite(models.Model):
    """
    Represents extended site information associated with a Django Site.

    This model stores extended information about a Django Site, including metadata,
    logos, contact details, and social media links.

    Attributes:
        site (Site): One-to-One relationship with the Django Site model.
        site_meta (str): Meta information for the site.
        site_description (str): A longer description for the site.
        site_meta_tag (str): Meta tag for the site.
        site_favicon (ImageField): Site favicon image.
        site_logo (ImageField): Site logo image.
        slogan (str): A short slogan or tagline for the site.
        og_image (ImageField): Open Graph image for social sharing.
        mask_icon (FileField): SVG file for mask icon.

        phone (str): Contact phone number.
        email (EmailField): Contact email address.
        location (str): Physical location or address.
        facebook_link (URLField): Facebook profile URL.
        twitter_link (URLField): Twitter profile URL.
        linkedin_link (URLField): LinkedIn profile URL.

        qualified_ans_range (int): A numeric value representing a qualification range.

    Managers:
        objects (models.Manager): The default manager.
        on_site (CurrentSiteManager): Manager for filtering by the current site.

    Methods:
        __str__(): Returns a string representation of the ExSite instance.

    """
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
    
    
    qualified_ans_range = models.IntegerField(default=1)
    
    # It is implemented for future roadmap
    objects = models.Manager()
    on_site = CurrentSiteManager('site')
    
    def __str__(self):
        return self.site.__str__()  

def apps_choice():
    """
    Generates a list of choices for the 'apps' field in Acordion model.

    This function retrieves the verbose names of all installed apps in the project
    and generates choices for the 'apps' field in the Acordion model.

    Returns:
        list: A list of tuples containing choices in the format ('slugified_name', 'Verbose Name').
    """
    PROJECT_APPS = [app.verbose_name for app in apps.get_app_configs()]    
    al = []
    for pa in PROJECT_APPS:        
        tc = (            
            slugify(pa) , pa,        )
        al.append(tc)        
    return al

class Acordion(models.Model):
    """
    Represents an accordion element with a button and description.

    This model represents an accordion element that typically contains a button
    with text and a description. It also allows associating the accordion element
    with a choice of installed apps.

    Attributes:
        button_text (str): Text displayed on the button.
        button_des (str): Description or content associated with the accordion element.
        apps (str): Choice field for associating the accordion with an installed app.

    Methods:
        __str__(): Returns a string representation of the Acordion instance.

    """
    button_text = models.CharField(max_length=256)
    button_des = models.TextField()
    apps = models.CharField(max_length=50, choices=apps_choice())    
    
    def __str__(self):
        return self.button_text