from django.db import models
from django.urls import reverse


class GuideType(models.Model):
    """
    Model representing different types of guides.

    Attributes:
        title (CharField): The title of the guide type.
        position (IntegerField): The position of the guide type.
        key (SlugField): A slug field used for identifying the guide type.
        icon_image (ImageField): An image field for the guide type's icon.
    """
    title = models.CharField(max_length=252)
    position = models.IntegerField()
    key = models.SlugField()
    icon_image = models.ImageField(upload_to = 'guideicon/')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """
        Get the absolute URL for a guide type.

        Returns:
            str: The absolute URL for the guide type.
        """
        return reverse('guide:guide_type', kwargs={'key': str(self.key)})    
    
class GuideMenu(models.Model):
    """
    Model representing menus for guides.

    Attributes:
        title (CharField): The title of the guide menu.
        position (IntegerField): The position of the guide menu.
        guidetype (ForeignKey): A foreign key to the associated guide type.
        slug (SlugField): A slug field used for identifying the menu.
    """
    title = models.CharField(max_length=252)   
    position = models.IntegerField()
    guidetype = models.ForeignKey(GuideType, on_delete=models.CASCADE, related_name='typeofguide')
    slug = models.SlugField() 
    
    
    def __str__(self):
        return self.title 
    
    def get_absolute_url(self):
        """
        Get the absolute URL for a general guide.

        Returns:
            str: The absolute URL for the general guide.
        """
        return reverse('guide:genarel_guide', kwargs={'slug': str(self.slug), 'gt': str(self.guidetype.key)})     
    

class GenarelGuide(models.Model):
    """
    Model representing general guides.

    Attributes:
        title (CharField): The title of the general guide.
        position (IntegerField): The position of the general guide.
        menu (ForeignKey): A foreign key to the related guide menu.
        anchor (CharField): An anchor field.
        parent (ForeignKey): A foreign key to a parent guide (self-referential relationship).
        content (TextField): The content of the general guide.
    """
    title = models.CharField(max_length=252)
    position = models.IntegerField()
    menu = models.ForeignKey(GuideMenu, on_delete=models.CASCADE, related_name='menuofguide')    
    anchor = models.CharField(max_length=252)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True, related_name='menuchild', limit_choices_to={'parent': None} )    
    content = models.TextField()
    
    def __str__(self):
        
        if self.parent:
            parent = f'It is child of Parent "{str(self.parent.title)}" of {self.menu.guidetype.title}' 
        else:
            parent = f'It is Parent  of {self.menu.guidetype.title}'
        
        
        return  self.title + ' -- ' + parent