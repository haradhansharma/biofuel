from django.db import models
from django.urls import reverse


class GuideType(models.Model):
    title = models.CharField(max_length=252)
    position = models.IntegerField()
    key = models.SlugField()
    icon_image = models.ImageField(upload_to = 'guideicon/')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('guide:guide_type', kwargs={'key': str(self.key)})    
    
class GuideMenu(models.Model):
    title = models.CharField(max_length=252)   
    position = models.IntegerField()
    guidetype = models.ForeignKey(GuideType, on_delete=models.CASCADE, related_name='typeofguide')
    slug = models.SlugField() 
    
    
    def __str__(self):
        return self.title 
    
    def get_absolute_url(self):
        return reverse('guide:genarel_guide', kwargs={'slug': str(self.slug), 'gt': str(self.guidetype.key)})     
    

class GenarelGuide(models.Model):
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