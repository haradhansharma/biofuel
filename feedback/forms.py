from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
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
        # Set the value of the hidden field before calling the parent save method
        instance = super().save(commit=False)
        instance.url = self.cleaned_data['url']
        if commit:
            instance.save()
        return instance