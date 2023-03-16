from django import forms
from accounts.models import User, Profile
from evaluation.models import Question, Option, Suggestions, NextActivities
from django.contrib.auth.forms import PasswordChangeForm
from home.models import Quotation
from django.forms.models import (
    inlineformset_factory, 
    formset_factory, 
    modelform_factory, 
    modelformset_factory
)
from evaluation.helper import get_sugested_questions

class PasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'})
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'})
        
    





class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name', 'email', 'orgonization', 'phone', )        
        widgets = {                      
            'username': forms.TextInput(attrs={'placeholder': 'username', 'class':'form-control', 'aria-label':'username',  }),
            'first_name': forms.TextInput(attrs={'placeholder': 'first name', 'class':'form-control', 'aria-label':'first name' }),
            'last_name': forms.TextInput(attrs={'placeholder': 'last name','class':'form-control', 'aria-label':'last name', }), 
            'orgonization': forms.TextInput(attrs={'placeholder': 'orgonization','class':'form-control', 'aria-label':'orgonization', }), 
            'phone': forms.TextInput(attrs={'placeholder': 'phone','class':'form-control', 'aria-label':'phone', }), 
            'email': forms.EmailInput(attrs={'placeholder': 'email', 'class':'form-control', 'aria-label':'email' , }),              
        }
        labels = {     
                     
            'username':'Username',
            'first_name':'First name',
            'last_name':'Last Name',
            'orgonization':'Orgonization',
            'phone':'Phone',
            'email': 'Email',
            
        }
        
        
class CompanyLogoForm(forms.ModelForm):
    class Meta:
        
        
        model = Profile
        fields = ('company_logo',)
        
        widgets = {  
            'avatar': forms.FileInput(attrs={ 'class':'form-control', 'aria-label':'company_logo' }),   
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
        
        
class SugestionForm(forms.ModelForm):
    class Meta:
        model = Suggestions
        fields = (
            
            'su_type',
            'title',
            'statement',
            
        )
        widgets = {
            
            'su_type' : forms.Select(attrs={ 'class':'form-select', 'aria-label':'Sugestion Type', 'placeholder':'Select SUgestion Type' }), 
            'title' : forms.TextInput(attrs={'class':'form-control', 'aria-label':'Title ', 'placeholder':'Title'}),
            'statement': forms.Textarea(attrs={'rows': 3,'class':'form-control', 'aria-label':'Statement' , 'placeholder':'Statement or Description' }),
        }
        
        
class QuesSugestionForm(forms.ModelForm):
    # parent = forms.ModelChoiceField(queryset=Suggestions.objects.filter())
    

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")       
        super().__init__(*args, **kwargs)    
  
        self.fields['related_qs'].choices = [(ch.pk, ch) for ch in get_sugested_questions(self.request)]
        self.fields['related_qs'].choices.insert(0, (None, '-----'))
        
    class Meta:
        model = Suggestions
        fields = (
            'su_type',
            'title',
            'statement',
            'related_qs'
        )
        
        widgets = {
            
            'su_type' : forms.Select(attrs={ 'class':'form-select', 'aria-label':'Sugestion Type', 'placeholder':'Select SUgestion Type' }), 
            'title' : forms.TextInput(attrs={'class':'form-control', 'aria-label':'Title ', 'placeholder':'Title'}),
            'statement': forms.Textarea(attrs={'rows': 3,'class':'form-control', 'aria-label':'Statement' , 'placeholder':'Statement or Description' }),
            'related_qs' : forms.Select(attrs={ 'class':'form-select', 'aria-label':'Sugestion Type', 'placeholder':'Select Related Question' }), 
            
        }
      
  
class NextActivitiesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")       
        super().__init__(*args, **kwargs)   
    class Meta:
        model = NextActivities
        fields = (
            'name_and_standared',
            'short_description',
            'descriptions',
            'url',
            'priority',
            'related_questions',
            'compulsory_questions',
            'related_percent',
            'compulsory_percent',
            'is_active',
        )
        
        widgets = {
            
            'related_questions' : forms.SelectMultiple(attrs={ 'class':'form-select', 'aria-label':'Related questions', 'size': 10 }), 
            'compulsory_questions' : forms.SelectMultiple(attrs={ 'class':'form-select', 'aria-label':'Compolsury questions', 'size': 10 }), 
            
            'name_and_standared' : forms.TextInput(attrs={'class':'form-control', 'aria-label':'name_and_standared ', 'placeholder':'Name And Standared. ex: ISO 8217:2017 test, LCA Analysis etc'}),
            'priority' : forms.TextInput(attrs={'class':'form-control', 'aria-label':'priority ', 'placeholder':'Priority ex: 1, 2, 3, 4 etc'}),
            
            # 'related_percent' : forms.TextInput(attrs={'class':'form-control', 'aria-label':'related_percent ', 'placeholder':'Related Percent ex: 90%'}),
            # 'compulsory_percent' : forms.TextInput(attrs={'class':'form-control', 'aria-label':'compulsory_percent ', 'placeholder':'Compulsory Percent ex: 80%'}),
            
            
            'short_description': forms.Textarea(attrs={'rows': 2,'class':'form-control', 'aria-label':'Short Descriptions' , 'placeholder':'Short Descriptions about test' }),
            'descriptions': forms.Textarea(attrs={'rows': 4,'class':'form-control', 'aria-label':'Descriptions' , 'placeholder':'Long Descriptions about test' }),
            'url' : forms.URLInput(attrs={'class':'form-control', 'aria-label':'url ', 'placeholder':'Write related URL to the test ex: https://example.com'}),
            
            # 'related_qs' : forms.Select(attrs={ 'class':'form-select', 'aria-label':'Sugestion Type', 'placeholder':'Select Related Question' }), 
            
        }
        
        
        
        
      

        
       
  
  
        
  
  
       