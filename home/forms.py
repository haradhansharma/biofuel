from django import forms
import json
from django.conf import settings
from django.db.models import Q
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
from django.core.mail import mail_admins, send_mail
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
      
#Below form is dedicated to a specific view which is "add_new_service" of Home
# So if you want to use this please look into the over written "save" method

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
            'related_percent',
            'compulsory_percent',
            
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
            'related_percent' : forms.HiddenInput(),
            'compulsory_percent' : forms.HiddenInput(),

            
            # 'related_qs' : forms.Select(attrs={ 'class':'form-select', 'aria-label':'Sugestion Type', 'placeholder':'Select Related Question' }), 
            
        }
        
    def save(self, commit=True):
        # going to check if saved service is exists or not which are going to be saved now        
        
        
        related_questions_ids = (self.cleaned_data['related_questions']).values_list('id', flat=True).order_by('id')       
        compulsory_questions_ids = (self.cleaned_data['compulsory_questions']).values_list('id', flat=True).order_by('id') 
          
        forms_selecetd_ids = (related_questions_ids.union(compulsory_questions_ids)).order_by('id')
        
        all_saved_instance = self._meta.model.objects.all().order_by('id')
        
        
 
        existing_instance = None        
        for ai in all_saved_instance:          
            if str(forms_selecetd_ids) == str(ai.selected_ids):
                existing_instance = ai    
                break  
            
        
            
                
            
        
        # modifying the existing save method's return to indicate wherether found or not
        if existing_instance is not None:
            if not existing_instance.is_active:
                
                
                #update user id at same_tried_by
                same_tried_by = existing_instance.same_tried_by
                if same_tried_by:
                    same_tried_by_json = json.loads(same_tried_by)   
                    tried_users = list(same_tried_by_json['users'])
                    if self.request.user.id not in tried_users:
                        tried_users.append(self.request.user.id)
                    data = {
                        'users' : tried_users
                    }
                else:                    
                    data = {
                        'users' : [self.request.user.id]
                    }
                existing_instance.same_tried_by = json.dumps(data)   
                existing_instance.save()
                
                #send notification to admin
                admins = User.objects.filter(is_staff=True)
                for admin in admins:
                    subject = f' Service "{existing_instance.name_and_standared}"- was tried by {self.request.user.username}, Please approve it!'
                    message = 'Hello {},\n\nThis is an important notification about the new service which is not approved yet but users tried to add their service list! Details mentioned in the message subject. You may take action to approve it.\n\nBest regards,\nAdmin Team'.format(admin.username)
                    from_email = settings.DEFAULT_FROM_EMAIL
                    recipient_list = [admin.email]
                    send_mail(subject, message, from_email, recipient_list)   
                
            context = {
                'existing_found' : True,
                'instance' : existing_instance
            }
            return context
        else:        
            instance = super().save(commit=False)
            # do something else with the instance
            if commit:
                instance.save()
                
                
            context = {
                'existing_found' : False,
                'instance' : instance
            }
            return context
        
        
        
        
      

        
       
  
  
        
  
  
       