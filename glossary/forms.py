from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox
from django.core.exceptions import ValidationError

from .models import *


class GRequestsChangeForm(forms.ModelForm):
    """
    Form for changing GRequests model data.

    This form is used for changing the data of the GRequests model. It includes a custom
    validation for the 'description' field to ensure it is not empty.

    Attributes:
        Meta: A nested class defining metadata options for the form.
    """
    
    
    class Meta:
        model = GRequests
        fields = '__all__'
        
        

    def clean(self, *args, **kwargs):
        """
        Custom clean method for validating the 'description' field.

        This method checks if the 'description' field is empty and raises a
        forms.ValidationError if it is.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A cleaned data dictionary.
        """
        description = self.cleaned_data.get('description')
        
        if description == '':
            raise forms.ValidationError("Description Required")
        
        return super(GRequestsChangeForm, self).clean(*args, **kwargs)


class GRequestForms(forms.ModelForm):   
    """
    Form for submitting GRequests with a CAPTCHA.

    This form is used for submitting GRequests and includes CAPTCHA validation.
    It also provides custom labels and widgets for the form fields.

    Attributes:
        captcha: A ReCaptchaField instance for CAPTCHA validation.
        Meta: A nested class defining metadata options for the form.
    """
    
    
    captcha = ReCaptchaField( widget=ReCaptchaV2Checkbox) 
    
    
    class Meta:
        model = GRequests
        fields = ['title', 'captcha']
        
        widgets = {                      
            'title': forms.TextInput(attrs={'title':'Title', 'class':'form-control', 'aria-label':'Title' }),
        }
        
        labels = {  
            'title': 'Looking for a definition that is not here? Submit your own search term.',       
            
        }
        
    def clean(self, *args, **kwargs): 
        """
        Custom clean method for validating CAPTCHA and 'title' fields.

        This method checks if the CAPTCHA and 'title' fields are empty and raises
        forms.ValidationErrors if they are.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A cleaned data dictionary.
        """
        
        
        captcha = self.cleaned_data.get('g-recaptcha-response')  
        title = self.cleaned_data.get('title')       
             
     
        
        # Check if CAPTCHA is empty and raise a validation error if it is.
        if captcha == '':
            raise forms.ValidationError("Captcha Check required")    
        
        # Check if 'title' is empty and raise a validation error if it is.
        if title == '':
            raise forms.ValidationError("Title Check required")          
                 
                                    
        return super(GRequestForms, self).clean(*args, **kwargs)
       