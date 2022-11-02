from django import forms
from .models import *
from django.utils.translation import gettext as _
#Standalone form for evaluation index page
class EvaluatorForm(forms.ModelForm):
 
    class Meta:
        model = Evaluator
        fields = ('name', 'email', 'phone', 'orgonization', 'biofuel')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'your name', 'class':'form-control', 'aria-label':'name' }),
            'email': forms.EmailInput(attrs={'placeholder': 'your email', 'class':'form-control', 'aria-label':'email' }),
            'orgonization': forms.TextInput(attrs={'placeholder': 'Organization', 'class':'form-control', 'aria-label':'orgonization', }), 
            'phone': forms.TextInput(attrs={'placeholder': 'your phone', 'class':'form-control', 'aria-label':'phone'}),
            'biofuel': forms.Select(attrs={'class':'form-select', 'aria-label':'biofuel', 'hx-get':'/evaluation/stdoils/', 'hx-target': '#stdoil',  'hx-indicator':".oilindicator" }),
                      
        }
        
        
        labels = {  
            'name': _('Name'),
            'email': _('Email'),
            'orgonization': _('Organization'),
            'phone': _('Phone'),
            'biofuel': _('Select Biofuel'),
            'stdoils': _('Select Related Oil'),
            
        }
    
    
    