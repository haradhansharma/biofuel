# from accounts.models import User
from django.db import models
from django.urls import reverse
from evaluation.models import Question, NextActivities
from django.core.validators import FileExtensionValidator
from django.conf import settings

User = settings.AUTH_USER_MODEL


class PriceUnit(models.Model):
    name = models.CharField(max_length=5)
    
    def __str__(self):
        return self.name
    
class TimeUnit(models.Model):
    name = models.CharField(max_length=5)
    
    def __str__(self):
        return self.name
    
    
class WeightUnit(models.Model):
    name = models.CharField(max_length=5)
    
    def __str__(self):
        return self.name
    
class QuotationDocType(models.Model):
    name = models.CharField(max_length=152)
    
    def __str__(self):
        return self.name



class Quotation(models.Model): 
    
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotationserviceprovider')   
    price = models.DecimalField(verbose_name='Quotation Price' , help_text='Write the proper price and remember to choose the appropriate pricing unit from the options next to the price box.', decimal_places=2, max_digits=10)
    price_unit = models.ForeignKey(PriceUnit, verbose_name='Price Unit', on_delete=models.CASCADE, related_name='priceunitquatation')
    needy_time = models.IntegerField(verbose_name='Total needed time for the test', help_text="Write the proper needy time to conduct the test and remember to choose the appropriate time unit from the options next to the needy time box.")
    needy_time_unit = models.ForeignKey(TimeUnit, verbose_name='Time Unit', on_delete=models.CASCADE, related_name='timeunitquatation')
    sample_amount = models.IntegerField(verbose_name="Sample amount needed for test", help_text="Note how much sample you need to perform this test. Do not forget to select the unit of weight.")
    sample_amount_unit = models.ForeignKey(WeightUnit, verbose_name='Weight Unit', on_delete=models.CASCADE, related_name='weightunitquatation')
    require_documents = models.ManyToManyField(QuotationDocType, verbose_name='Document needed for test',help_text="Select the documents you need to perform this test. Can select multiple. Hold down “Control”, or “Command” on a Mac, to select more than one.", related_name='requiredocuments')
    factory_pickup = models.BooleanField(verbose_name="Factory Sample pick-up", help_text="Place a tick mark to indicate whether the sample will be collected from the factory.")
    test_for = models.ForeignKey(Question, verbose_name="Tests for question", help_text="Help Text will go here", max_length=252, on_delete=models.CASCADE, related_name='testfor', limit_choices_to={'is_active': True, 'is_door' : False})
    related_questions = models.ManyToManyField(Question, verbose_name="Please select all other question which are also tested within the provided quotation", help_text="Allow multiple option selection. The selected options should be highlighted.", limit_choices_to={'is_active': True, 'is_door' : False})
    quotation_format = models.FileField(upload_to="quotation", help_text="Only '.pdf' are allowed", verbose_name="Upload Quotation (pdf)", validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    next_activities = models.ForeignKey(NextActivities, help_text="Select next activities to select related questions from next activities", on_delete=models.PROTECT, related_name='quotnextactivity', null=True, blank=True, unique=False)
    display_site_address = models.BooleanField(default=True, verbose_name="Display Site Address", help_text="Tick will display system address IO Validation partner address")
    comments = models.TextField(max_length=500, help_text="This field will take charecter upto 500", null=True, blank=True)
    
    def __str__(self):
        return str(self.service_provider) + str(self.id)
    
    @property
    def get_quot_url(self):
        return reverse('home:add_quatation', args=[str(self.test_for.slug)])
    
    def get_absolute_url(self):        
        return reverse('home:quotation_report', kwargs={'question': str(self.test_for.slug), 'quotation': int(self.id) })      
    
     
