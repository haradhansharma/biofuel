from django import forms




class UploadLead(forms.Form):
    lead_upload = forms.FileField()
    
    
class SubscriberForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Your Name'}))
    email = forms.EmailField(label='Your email', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Your Email'}))