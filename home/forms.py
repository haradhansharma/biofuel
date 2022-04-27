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
                      
            'about': forms.Textarea(attrs={'placeholder': 'about', 'class':'form-control', 'aria-label':'about' }),
            'location': forms.TextInput(attrs={'placeholder': 'location', 'class':'form-control', 'aria-label':'location' }),
            'established': forms.DateInput(attrs={'data-datepicker': "" , 'class':'form-control', 'aria-label':'established', }), 
            
            
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
                      
            'name': forms.TextInput(attrs={'placeholder': 'name', 'class':'form-control', 'aria-label':'name' }),          
            
            
        }
        
        labels = {     
                     
            'name': 'Edit Question',
            
                     
        }
        

class OptionForm(forms.ModelForm):
    class Meta:
        model   = Option
        fields  = ('name', 'statement', )
        widgets = {                      
            'name': forms.TextInput(attrs={'placeholder': 'name', 'class':'form-control', 'aria-label':'name' }),
            'statement': forms.Textarea(attrs={'placeholder': 'statement', 'class':'form-control', 'aria-label':'statement' }),            
            
        }
        
        labels = {     
                     
            'name': 'Option Label',
            'statement': 'Option Statement',
                     
        }
        
class QuotationForm(forms.ModelForm):
    
    
    # def __init__(self, *args,**kwargs):        
    #     from home.views import get_question_of_label
    #     self.request = kwargs.pop('request', None)
    #     print(self.request)
    #     super (QuotationForm, self ).__init__(*args,**kwargs) # populates the post
        
        # self.fields['related_questions'].queryset = get_question_of_label(request)
        
    
    class Meta:
        model = Quotation
        fields = ('price', 'price_unit', 'needy_time', 'needy_time_unit', 'sample_amount', 'sample_amount_unit', 'require_documents', 'factory_pickup', 'test_for',  'related_questions', 'quotation_format',   )
        
    
        
        widgets = {                      
            'price': forms.TextInput(attrs={'class':'form-control', 'aria-label':'price' , 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid "}),
            'price_unit': forms.Select(attrs={ 'class':'form-select', 'aria-label':'unit', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),  
            'needy_time': forms.TextInput(attrs={'class':'form-control', 'aria-label':'time', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),
            'needy_time_unit': forms.Select(attrs={ 'class':'form-select', 'aria-label':'time', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),     
            'sample_amount': forms.TextInput(attrs={'class':'form-control', 'aria-label':'amount', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),
            'sample_amount_unit': forms.Select(attrs={ 'class':'form-select', 'aria-label':'amount', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),      
            'require_documents': forms.Select(attrs={ 'class':'form-select', 'aria-label':'documents', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),   
            'factory_pickup': forms.CheckboxInput(attrs={ 'class':'form-check-input', 'aria-label':'pickup' }),   
            'test_for': forms.Select(attrs={'class':'form-select', 'aria-label':'test', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid "}),      
            'related_questions': forms.SelectMultiple(attrs={ 'class':'form-select', 'aria-label':'documents', 'style':"border: None; box-shadow: None; border-radius:0; border-bottom:1px solid " }),   
            'quotation_format': forms.FileInput(attrs={ 'class':'form-control', 'aria-label':'file' }),           
        }


  
    

        
       
  
  
        
  
  
       