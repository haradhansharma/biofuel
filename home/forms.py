from django import forms
from accounts.models import User, Profile
from evaluation.models import Question, Option

from django.contrib.auth.forms import PasswordChangeForm

from home.models import Quotation


class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class':'form-control'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'})
        





class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'orgonization', 'phone', )        
        widgets = {
                      
            'username': forms.TextInput(attrs={'placeholder': 'username', 'class':'form-control', 'aria-label':'username',  }),
            'first_name': forms.TextInput(attrs={'placeholder': 'first_name', 'class':'form-control', 'aria-label':'first_name' }),
            'last_name': forms.TextInput(attrs={'placeholder': 'last_name','class':'form-control', 'aria-label':'last_name', }), 
            'orgonization': forms.TextInput(attrs={'placeholder': 'orgonization','class':'form-control', 'aria-label':'orgonization', }), 
            'phone': forms.TextInput(attrs={'placeholder': 'phone','class':'form-control', 'aria-label':'phone', }), 
            'email': forms.EmailInput(attrs={'placeholder': 'email', 'class':'form-control', 'aria-label':'email' , }),            
            
        }
        labels = {     
                     
            'username':'Username',
            'first_name':'First name',
            'first_name':'Last Name',
            'orgonization':'Orgonization',
            'phone':'Phone',
            'email': 'Email',
            
        }
        
        
   
        
class ProfileForm(forms.ModelForm):
    class Meta:
        
        
        model = Profile
        fields = ('about','location','established',)
        
        widgets = {
                      
            'about': forms.Textarea(attrs={'placeholder': 'About', 'class':'form-control', 'aria-label':'about' }),
            'location': forms.TextInput(attrs={'placeholder': 'Location', 'class':'form-control', 'aria-label':'location' }),
            'established': forms.DateInput(format='%d-%m-%Y', attrs={ 'placeholder':"Select a Date", 'class':'form-control', 'aria-label':'established', }), 
            
            
        }
        labels = {     
                     
            'about': 'About',
            'location': 'Location',
            'established': 'Established',           
            
        }
        
class QuestionForm(forms.ModelForm):
    class Meta:
        model   = Question
        fields  = ('name',)
        widgets = {                      
            'name': forms.TextInput(attrs={'placeholder': 'Title of the question', 'class':'form-control', 'aria-label':'name' }),     
        }
        
        labels = { 
                     
            'name': 'Edit Question',          
                     
        }
        

class OptionForm(forms.ModelForm):
    class Meta:
        model   = Option
        fields  = ('name', 'statement', )
        widgets = {                      
            'name': forms.TextInput(attrs={'placeholder': 'Label of the Option', 'class':'form-control', 'aria-label':'name' }),
            'statement': forms.Textarea(attrs={'placeholder': 'Statement for the option', 'class':'form-control', 'aria-label':'statement' }),            
            
        }
        
        labels = {     
                     
            'name': 'Option Label',
            'statement': 'Option Statement',
                     
        }
        
class QuotationForm(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ('price', 'price_unit', 'needy_time', 'needy_time_unit', 'sample_amount', 'sample_amount_unit', 'require_documents', 'factory_pickup', 'test_for',  'related_questions', 'quotation_format', 'next_activities', 'display_site_address', 'show_alternate_email', 'show_alternate_business', 'show_alternate_phone', 'comments', )
        
    
        
        widgets = {                      
            'price': forms.TextInput(attrs={'class':'form-control', 'aria-label':'price' , 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid "}),
            'price_unit': forms.Select(attrs={ 'class':'form-select', 'aria-label':'unit', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),  
            'needy_time': forms.TextInput(attrs={'class':'form-control', 'aria-label':'time', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),
            'needy_time_unit': forms.Select(attrs={ 'class':'form-select', 'aria-label':'time', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),     
            'sample_amount': forms.TextInput(attrs={'class':'form-control', 'aria-label':'amount', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),
            'sample_amount_unit': forms.Select(attrs={ 'class':'form-select', 'aria-label':'amount', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),      
            'require_documents': forms.SelectMultiple(attrs={ 'class':'form-select', 'aria-label':'documents', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),   
            'factory_pickup': forms.CheckboxInput(attrs={ 'class':'form-check-input', 'aria-label':'pickup' }),   
            'test_for': forms.Select(attrs={'class':'form-select', 'aria-label':'test', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid "}),      
            'related_questions': forms.SelectMultiple(attrs={ 'class':'form-select', 'aria-label':'documents', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid; border-top:1px solid; height:200px; " }),   
            'quotation_format': forms.FileInput(attrs={ 'class':'form-control', 'aria-label':'file' }), 
            'next_activities': forms.Select(attrs={ 'class':'form-select', 'aria-label':'unit', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),            
            'display_site_address': forms.CheckboxInput(attrs={ 'class':'form-check-input', 'aria-label':'address' }),    
            'show_alternate_email': forms.TextInput(attrs={'class':'form-control', 'aria-label':'show_alternate_email' , 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid "}),
            'show_alternate_phone': forms.TextInput(attrs={'class':'form-control', 'aria-label':'show_alternate_email' , 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid "}),            
            'show_alternate_business': forms.TextInput(attrs={'class':'form-control', 'aria-label':'show_alternate_business' , 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid "}),                 
            'comments': forms.Textarea(attrs={'rows': 3,'class':'form-control', 'aria-label':'Comments' , }),
            
            # 'next_activities': forms.Select(attrs={ 'class':'form-select', 'aria-label':'unit', 'hx-post':"#", 'hx-trigger':"change", 'hx-swap':"outerHTML", 'hx-target':'#pppp', 'hx-vals':'{"changing_activity": "{question.slug}"}', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),          
        }
class NextActivitiesOnQuotation(forms.ModelForm):
    class Meta:
        model = Quotation
        fields = ('next_activities',)
        widgets = {
            'next_activities': forms.Select(attrs={ 'class':'form-select', 'aria-label':'unit', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),
        }
      
  
    

        
       
  
  
        
  
  
       