from django.db import models
from django.urls import reverse
from evaluation.models import Question
from django.core.validators import FileExtensionValidator
from django.conf import settings
from accounts.models import User

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
    price = models.DecimalField(verbose_name='Quotation Price' , help_text='Help text will go here', decimal_places=2, max_digits=10)
    price_unit = models.ForeignKey(PriceUnit, verbose_name='Price Unit', on_delete=models.CASCADE, related_name='priceunitquatation')
    needy_time = models.IntegerField(verbose_name='Total needed time for the test', help_text="Help Text will go")
    needy_time_unit = models.ForeignKey(TimeUnit, verbose_name='Time Unit', on_delete=models.CASCADE, related_name='timeunitquatation')
    sample_amount = models.IntegerField(verbose_name="Sample amount needed for test", help_text="Help Text will go here")
    sample_amount_unit = models.ForeignKey(WeightUnit, verbose_name='Weight Unit', on_delete=models.CASCADE, related_name='weightunitquatation')
    require_documents = models.ForeignKey(QuotationDocType, verbose_name='Document needed for test',help_text="Help Text will go", on_delete=models.CASCADE, related_name='requiredocuments')
    factory_pickup = models.BooleanField(verbose_name="Factory Sample pick-up", help_text="Help Text will go")
    test_for = models.ForeignKey(Question, verbose_name="Tests for question", help_text="Help Text will go here", max_length=252, on_delete=models.CASCADE, related_name='testfor', limit_choices_to={'is_active': True, 'is_door' : False})
    related_questions = models.ManyToManyField(Question, verbose_name="Please select all other question which are also tested within the provided quotation", help_text="Help Text will go here", limit_choices_to={'is_active': True, 'is_door' : False})
    quotation_format = models.FileField(upload_to="quotation", help_text="Only '.pdf' are allowed", verbose_name="Upload Quotation (pdf)", validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    
    def __str__(self):
        return str(self.service_provider) + str(self.id)
    
    @property
    def get_quot_url(self):
        return reverse('home:add_quatation', args=[str(self.test_for.slug)])
