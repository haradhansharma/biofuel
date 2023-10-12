from django.db import models
from django.template.defaultfilters import slugify

class Glossary(models.Model):
    """
    Model representing glossary entries.

    This model stores information about glossary entries, including their title,
    description, and automatically generated slug and anchor fields.

    Attributes:
        created (DateTimeField): The date and time when the entry was created (auto-generated).
        modified (DateTimeField): The date and time when the entry was last modified (auto-generated).
        title (CharField): The title of the glossary entry.
        slug (SlugField): A unique slug based on the title (auto-generated).
        anchor (SlugField): A non-unique slug derived from the first character of the title (auto-generated).
        description (TextField): The description or definition of the glossary entry.

    Methods:
        __str__: A string representation of the glossary entry, using its title.
        save: Custom save method to generate the slug and anchor fields based on the title.

    Meta:
        ordering (list): Default ordering for glossary entries, first by title, then by modification date.
    """
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, editable=False)
    anchor = models.SlugField(unique=False, editable=False)
    description = models.TextField()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):  
        """
        Custom save method to generate the slug and anchor fields based on the title.
        """
        key_sample = slugify(self.title)    
        self.slug = key_sample
        anchor = self.title[0]
        self.anchor = anchor.upper()
        super(Glossary, self).save(*args, **kwargs)

    class Meta:
        ordering = ['title', '-modified']
    
class RelatedLinks(models.Model):
    """
    Model representing related links for glossary entries.

    This model stores information about related links associated with glossary entries,
    including their title, URL link, and a foreign key to the related glossary entry.

    Attributes:
        title (CharField): The title of the related link.
        link (URLField): The URL link.
        glossary (ForeignKey): A foreign key reference to the related glossary entry.

    Methods:
        __str__: A string representation of the related link, including the associated glossary entry's title.
    """
    title = models.CharField(max_length=250)
    link  = models.URLField()
    glossary  = models.ForeignKey(Glossary, related_name="relatedlinks", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} (link for {self.glossary.title})"
    
class GRequests(models.Model):
    """
    Model representing G Requests.

    This model stores information about G Requests, which are user-submitted requests
    for glossary entries.

    Attributes:
        created (DateTimeField): The date and time when the G Request was created (auto-generated).
        modified (DateTimeField): The date and time when the G Request was last modified (auto-generated).
        title (CharField): The title of the G Request.
        description (TextField, optional): Additional description or details of the request.

    Methods:
        __str__: A string representation of the G Request, using its title.

    Meta:
        verbose_name (str): The singular name for this model in the admin interface.
        verbose_name_plural (str): The plural name for this model in the admin interface.
    """
    
    class Meta:
        verbose_name = 'G Request'
        verbose_name_plural = 'G Requests'   
    
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    
    
    