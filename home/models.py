# from accounts.models import User
from django.db import models
from django.urls import reverse
from doc.doc_processor import site_info
from evaluation.models import Question, NextActivities
from django.core.validators import FileExtensionValidator
from django.conf import settings

User = settings.AUTH_USER_MODEL


class PriceUnit(models.Model):
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name
    
class TimeUnit(models.Model):
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name
    
    
class WeightUnit(models.Model):
    name = models.CharField(max_length=10)
    
    def __str__(self):
        return self.name
    
class QuotationDocType(models.Model):
    name = models.CharField(max_length=152)
    
    def __str__(self):
        return self.name


 
class Quotation(models.Model):     
    service_provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quotationserviceprovider', db_index=True)   
    show_alternate_email = models.EmailField(help_text='You can show alternate email address in quotation.', null=True, blank=True)
    show_alternate_business = models.CharField(help_text='You can show alternate email address in quotation.', max_length = 50, null=True, blank=True)    
    show_alternate_phone = models.CharField(help_text='You can show alternate phone number in quotation.', max_length = 50, null=True, blank=True)     
    price = models.DecimalField(verbose_name='Quotation Price' , help_text='Write the proper price and remember to choose the appropriate pricing unit from the options next to the price box.', decimal_places=2, max_digits=10)
    price_unit = models.ForeignKey(PriceUnit, verbose_name='Price Unit', on_delete=models.CASCADE, related_name='priceunitquatation')
    needy_time = models.IntegerField(verbose_name='Total needed time for the test', help_text="Write the proper needy time to conduct the test and remember to choose the appropriate time unit from the options next to the needy time box.")
    needy_time_unit = models.ForeignKey(TimeUnit, verbose_name='Time Unit', on_delete=models.CASCADE, related_name='timeunitquatation')
    sample_amount = models.IntegerField(verbose_name="Sample amount needed for test", help_text="Note how much sample you need to perform this test. Do not forget to select the unit of weight.")
    sample_amount_unit = models.ForeignKey(WeightUnit, verbose_name='Weight Unit', on_delete=models.CASCADE, related_name='weightunitquatation')
    require_documents = models.ManyToManyField(QuotationDocType, verbose_name='Document needed for test',help_text="Select the documents that are needed to perform this test. You can select multiple in mac by holding shift + command and down arrow and in windows ctrl/shift + down arrow.", related_name='requiredocuments')
    factory_pickup = models.BooleanField(verbose_name="Factory Sample pick-up", help_text="Place a tick mark to indicate whether the sample will be collected from the factory.")
    test_for = models.ForeignKey(
        Question, 
        verbose_name="Tests for question", 
        help_text="Help Text will go here", 
        db_index=True,
        max_length=252, 
        on_delete=models.CASCADE, 
        related_name='testfor', 
        limit_choices_to={'is_active': True, 'is_door' : False})
    related_questions = models.ManyToManyField(
        Question, 
        verbose_name="Please select all other question which are also tested within the provided quotation", 
        help_text="Allow multiple option selection. The selected options should be highlighted.", 
        limit_choices_to={'is_active': True, 'is_door' : False},
        db_index=True,        
        related_name='quotations_related_questions'
        )
    quotation_format = models.FileField(upload_to="quotation", help_text="Only '.pdf' are allowed", verbose_name="Upload Quotation (pdf)", validators=[FileExtensionValidator(allowed_extensions=['pdf'])])
    next_activities = models.ForeignKey(
        NextActivities, 
        help_text="Select next activities to select related questions from next activities", 
        on_delete=models.PROTECT, 
        db_index=True,        
        related_name='quotnextactivity', null=True, blank=True, unique=False)
    display_site_address = models.BooleanField(default=True, verbose_name="Display Site Address", help_text="Tick will display system address IO Validation partner address")
    comments = models.TextField(max_length=500, help_text="This field will take charecter upto 500", null=True, blank=True)
    
    def __str__(self):
        return str(self.service_provider) + str(self.id)
    
    @property
    def get_quot_url(self):
        return reverse('home:add_quatation', args=[str(self.test_for.slug)])
    
    @property
    def get_business_name(self):
        if self.display_site_address:
            business_name = site_info().get('name')
        else:
            if self.show_alternate_business:
                business_name = self.show_alternate_business
            else:
                if self.service_provider.orgonization:
                    business_name = self.service_provider.orgonization
                else:
                    business_name = 'Business Unknown'
        
        return business_name
    
    @property
    def get_phone(self):
        if self.display_site_address:
            phone = site_info().get('phone')
        else:
            if self.show_alternate_phone:
                phone = self.show_alternate_phone
            else:
                if self.service_provider.phone:
                    phone = self.service_provider.phone
                else:
                    phone = 'Phone Unknown'
        
        return phone
    
    @property
    def get_email(self):
        if self.display_site_address:
            email = site_info().get('email')
        else:
            if self.show_alternate_email:
                email = self.show_alternate_email
            else:
                if self.service_provider.email:
                    email = self.service_provider.email
                else:
                    email = 'email Unknown'
        
        return email
    
    def get_absolute_url(self):        
        return reverse('home:quotation_report', kwargs={'question': str(self.test_for.slug), 'quotation': int(self.id) })      
    
     
