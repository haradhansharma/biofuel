from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox
from django.core.exceptions import ValidationError

from .models import *


class GRequestsChangeForm(forms.ModelForm):
    class Meta:
        model = GRequests
        fields = '__all__'

    def clean(self, *args, **kwargs):
        description = self.cleaned_data.get('description')
        
        if description == '':
            raise forms.ValidationError("Description Required")
        return super(GRequestsChangeForm, self).clean(*args, **kwargs)


class GRequestForms(forms.ModelForm):   
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
        captcha = self.cleaned_data.get('g-recaptcha-response')  
        title = self.cleaned_data.get('title')       
             
     
        
        # to give more userfriendly experience.
        if captcha == '':
            raise forms.ValidationError("Captcha Check required")    
        if title == '':
            raise forms.ValidationError("Title Check required")          
                 
                                    
        return super(GRequestForms, self).clean(*args, **kwargs)
       