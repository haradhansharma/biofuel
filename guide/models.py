from django.db import models
from django.urls import reverse
from django_quill.fields import QuillField

class GuideType(models.Model):
    title = models.CharField(max_length=252)
    key = models.SlugField()
    icon_image = models.ImageField(upload_to = 'guideicon/')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('guide:guide_type', kwargs={'key': str(self.key)})    
    
class GuideMenu(models.Model):
    title = models.CharField(max_length=252)   
    type = models.ForeignKey(GuideType, on_delete=models.CASCADE, related_name='typeofguide')
    slug = models.SlugField() 
    
    
    def __str__(self):
        return self.title + ' -- ' + self.type.title
    
    def get_absolute_url(self):
        return reverse('guide:genarel_guide', kwargs={'slug': str(self.slug), 'type': str(self.type.key)})    
    

class GenarelGuide(models.Model):
    title = models.CharField(max_length=252)
    menu = models.ForeignKey(GuideMenu, on_delete=models.CASCADE, related_name='menuofguide')    
    anchor = models.CharField(max_length=252)
    parent = models.ForeignKey("guide.GenarelGuide", on_delete=models.CASCADE, null=True, blank=True, related_name='menuchild', limit_choices_to={'parent': None} )
    content = QuillField()
    
    def __str__(self):
        
        if self.parent:
            parent = f'It is child of Parent "{str(self.parent.title)}"' 
        else:
            parent = 'It is Parent'
        
        
        return  self.title + ' -- ' + parent