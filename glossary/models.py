from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.



class Glossary(models.Model):
    created     = models.DateTimeField(auto_now_add=True, editable=False)
    modified    = models.DateTimeField(auto_now=True, editable=False)
    title       = models.CharField(max_length=250)
    slug        = models.SlugField(unique=True, editable=False)
    anchor      = models.SlugField(unique=False, editable=False)
    description = models.TextField()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):  
        key_sample = slugify(self.title)    
        self.slug = key_sample
        anchor = self.title[0]
        self.anchor = anchor.upper()
        super(Glossary, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('django_glossary:term-detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title', '-modified']


    
class RelatedLinks(models.Model):
    title = models.CharField(max_length=250)
    link  = models.URLField()
    glossary  = models.ForeignKey(Glossary, related_name="relatedlinks", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} (link for {self.glossary.title})"

    # def get_absolute_url(self):
    #     return reverse('django_glossary:term-detail', kwargs={'slug': self.term.slug})
    
class GRequests(models.Model):
    
    created     = models.DateTimeField(auto_now_add=True, editable=False)
    modified    = models.DateTimeField(auto_now=True, editable=False)
    title       = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    
    
    