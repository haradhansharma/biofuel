from django import forms
from .models import *
from django.utils.translation import gettext as _


class EvaluatorForm(forms.ModelForm):
    """
    Form for creating and updating Evaluator instances.

    This form is used to create and update Evaluator instances based on the Evaluator model. It includes fields for
    'name', 'email', 'phone', 'organization', and 'biofuel'. It also defines widgets for each field to control its
    appearance in the HTML form.

    Args:
        forms.ModelForm: A form class that is automatically generated from the Evaluator model.

    Attributes:
        Meta (class): Inner class that defines metadata for the form, including the model and form fields.
        labels (dict): Custom labels for form fields.

    Methods:
        clean(self): Custom form validation to ensure 'biofuel' selection is mandatory.

    Example:
        To use this form in a view, you can create an instance of it as follows:

        form = EvaluatorForm(request.POST)

        After binding the form to request data, you can perform validation and save the Evaluator instance as needed.
    """
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
        """
        Custom form validation to ensure 'biofuel' selection is mandatory.

        This method is called during form validation to check if the 'biofuel' field has been selected. If 'biofuel'
        is not selected, a ValidationError is raised.

        Raises:
            forms.ValidationError: If 'biofuel' is not selected, this exception is raised with a relevant error message.
        """
        biofuel = self.cleaned_data.get('biofuel')           
        
        if not biofuel:
            raise forms.ValidationError(f'Fuel selction is mandatory!')
        
      
    
    
    