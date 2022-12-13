from django import forms
from .models import *
from django.utils.translation import gettext as _


class EvaluatorForm(forms.ModelForm):
    class Meta:
        model = Evaluator
        fields = ('name', 'email', 'phone', 'orgonization', 'biofuel')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'your name', 'class':'form-control', 'aria-label':'name', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'your email', 'class':'form-control', 'aria-label':'email', 'required': True }),
            'orgonization': forms.TextInput(attrs={'placeholder': 'Organization', 'class':'form-control', 'aria-label':'orgonization', }), 
            'phone': forms.TextInput(attrs={'placeholder': 'your phone', 'class':'form-control', 'aria-label':'phone'}),
            'biofuel': forms.Select(attrs={'class':'form-select', 'aria-label':'biofuel', 'hx-get':'/evaluation/stdoils/', 'hx-target': '#stdoil',  'hx-indicator':".oilindicator", 'required': True }),                      
        }        
        
        labels = {  
            'name': _('Name'),
            'email': _('Email'),
            'orgonization': _('Organization'),
            'phone': _('Phone'),
            'biofuel': _('Select Fuel'),
            'stdoils': _('Select Related Fuel Grade'),
            
        }
        
    def clean(self, *args, **kwargs):
        biofuel = self.cleaned_data.get('biofuel')           
        
        if not biofuel:
            raise forms.ValidationError(f'Fuel selction is mandatory!')
        
      
    
    
    