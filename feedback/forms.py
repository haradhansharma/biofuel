from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    """
    A Django form for the Feedback model.

    This form is used to collect and validate user feedback and store it
    in the Feedback model. It includes fields for 'name', 'phone', 'email',
    'url', and 'message', along with widget configurations for the form fields.

    Attributes:
        url (forms.URLField): A hidden field for capturing the URL from which
            feedback is submitted.
    """

    # Define the hidden 'url' field with a URL input widget.
    url = forms.URLField(widget=forms.HiddenInput())
    
    class Meta:
        model = Feedback
        fields = ('name', 'phone', 'email', 'url', 'message')  
        
        widgets = {                      
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class':'form-control', 'aria-label':'Name',  }),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone', 'class':'form-control', 'aria-label':'Phone',  }),            
            'email': forms.EmailInput(attrs={'placeholder': 'email', 'class':'form-control', 'aria-label':'email' , }), 
            'url': forms.TextInput(attrs={'placeholder': 'Url', 'class':'form-control', 'aria-label':'Url',  }),   
            'message': forms.Textarea(attrs={'rows':'5','placeholder': 'Message','class':'form-control', 'aria-label':'Message', }), 
        }
        
    def save(self, commit=True):
        """
        Save the feedback instance with the associated URL.

        This method overrides the parent save method to set the value of the
        hidden 'url' field before saving the instance to the database.

        Args:
            commit (bool): If True, save the instance to the database.

        Returns:
            Feedback: The saved Feedback instance.
        """
        # Create an instance of Feedback without saving it to the database yet.
        instance = super().save(commit=False)
        
         # Set the 'url' field from the cleaned_data before saving.
        instance.url = self.cleaned_data['url']
        if commit:
            # Save the instance to the database if commit is True.
            instance.save()
            
        return instance