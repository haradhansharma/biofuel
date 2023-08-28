from django import forms

class UploadLead(forms.Form):
    """
    A form for uploading lead data as a file.
    """
    lead_upload = forms.FileField() # A FileField to handle lead data uploads.
    
    
class SubscriberForm(forms.Form):
    """
    A form for collecting subscriber information.
    """
    name = forms.CharField(
        label='Your Name', max_length=20, 
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your Name'})
        ) # A CharField for the subscriber's name.
    
    email = forms.EmailField(
        label='Your email', max_length=100, 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Your Email'})
        ) # An EmailField for the subscriber's email.
    
    
