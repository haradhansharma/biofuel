from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.urls import reverse_lazy
from .models import User
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
# Part of googleee recaptcha.
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox




class UserCreationForm(UserCreationForm):
    
    #adding field to the admin template
    def __init__(self, *args, **kwargs): 
        super(UserCreationForm, self).__init__(*args, **kwargs)   
    UserAdmin.add_form = UserCreationForm
    UserAdmin.add_fieldsets = ((None, {
        'classes': ('wide',),
        'fields': ('usertype', 'email', 'phone', 'username', 'password1', 'password2',  'term_agree', 'experts_in', )
    }),)
        
        
    class Meta:
        model = User
        fields = '__all__'       
        
class UserCreationFormFront(UserCreationForm):
    
 
        
    
    #Inheriting and ading html property to default form of Django
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'term_agree', 'newsletter_subscription', 'usertype', 'experts_in',)  
              
    username = forms.CharField(label = 'Username',widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control", 'hx-post': reverse_lazy('accounts:check_username'), 'hx-target': '#username_error', 'hx-trigger': 'keyup[target.value.length > 3]' }))
    email = forms.EmailField(label = 'E-mail Address',  widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control" , 'hx-post': reverse_lazy('accounts:check_email'), 'hx-target': '#email_error', 'hx-trigger': 'keyup[target.value.length > 3]'}))
    password1 = forms.CharField(label = 'Password', widget=forms.PasswordInput(attrs={"placeholder": "Password","class": "form-control" }))
    password2 = forms.CharField(label = 'Confirm Password', widget=forms.PasswordInput(attrs={"placeholder": "Password check","class": "form-control"}))
    term_agree = forms.BooleanField(label = 'Agree Our', required=True,  widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    newsletter_subscription = forms.BooleanField(label = 'Subscribe to our newsletter', required=True,  widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    
    #implemeting google recapcha.
    captcha = ReCaptchaField( widget=ReCaptchaV2Checkbox)  
    
    widgets = {
            'usertype': forms.Select(attrs={ 'class':'form-select', 'aria-label':'usertype', 'hx-post':"/check_type_to_get_expert/", 'hx-trigger':"change", 'hx-target':"#hx" , 'hx-swap':"innerHTML"}),                    
            # 'experts_in': forms.Select(attrs={ 'class':'form-select', 'aria-label':'experts_in', }), 
            
        }
    
    def clean_username(self):
        data = self.cleaned_data.get('username')
        if " " in data:
            raise ValidationError("Space in username not allowed!")

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data
    
    def clean_experts_in(self):
        user_type = self.cleaned_data.get('usertype')
        data = self.cleaned_data.get('experts_in') 
        if user_type.is_expert:       
            if not data:
                raise ValidationError("Experts In Required!")
        return data
    
    # Inheriting default method of Django to customize for more interactiveness in front end
    def clean(self, *args, **kwargs):        
        username = self.cleaned_data.get('username')       
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email or password or username:            
            #check email verification                      
            email_qs = User.objects.filter(email=email)            
            if not email_qs.exists():
                pass
            else:
                '''
                if user already registered and nt verified the email,
                system will send activation mail again with message.
                as previous activation mail may be invalid or loss by user.
                '''        
                
                
                ver_email = User.objects.filter(email=email, email_verified=False)
                if ver_email.exists():
                    ver_email = ver_email.first()
                    subject = 'Email Verification Required!'  
                    current_site = Site.objects.get_current()  
                    message = render_to_string('emails/account_activation_email.html', {
                        'user': ver_email,                    
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(ver_email.pk)),
                        'token': account_activation_token.make_token(ver_email),                        
                    })                   
                    ver_email.email_user(subject, '', html_message=message)                   
                    raise forms.ValidationError(f'You have an account already with this email but email is not verified, your need to verify the email. An email verification link has been sent to your mailbox {email}') 
                else:   
                    '''
                    if email verified but not activated(It is happend for expert type of user)
                    will send curtesy mail and will show message.
                    
                    '''   
                    
                    
                    
                                                               
                    is_active_qs = User.objects.filter(email=email, is_active=False).first()                
                    if is_active_qs:  
                        if is_active_qs.is_expert or is_active_qs.is_marine:
                            raise forms.ValidationError("You have an account already with this email. But account is not activated by site admin, please wait for approval!")                              
                        else:             
                            subject = 'Account activation required!'  
                            current_site = Site.objects.get_current()  
                            message = render_to_string('emails/account_activation_email.html', {
                                'user': is_active_qs,                    
                                'domain': current_site.domain,
                                'uid': urlsafe_base64_encode(force_bytes(is_active_qs.pk)),
                                'token': account_activation_token.make_token(is_active_qs),                        
                            })                 
                            
                            is_active_qs.email_user(subject, '', html_message=message)                   
                            raise forms.ValidationError(f'You have an account already with this email, but email is not verified. An account activation link has been sent to your mailbox {email}')
        return super(UserCreationFormFront, self).clean(*args, **kwargs)  
    
    

class UserChangeForm(UserChangeForm):
    '''
    Inheriting dafault django form to give the facility to edit self account data.
    CVurrently it is being used in dashboard>>setting and dashboard>>password change form.
    '''
    class Meta:
        model = User
        fields = '__all__'
    widgets = {                              
            'email': forms.EmailInput(attrs={ 'class':'form-control', 'aria-label':'email' }),
        }
        

class LoginForm(AuthenticationForm):
    
    # Taking ccharge of default django form to customize and inserting custom HTML property.    
    
    
    username = forms.CharField(widget=forms.TextInput(attrs={ "class": "form-control" }))    
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))  
    
    
    # After saving cookie for 30 days as per current seting it will mark.  
    remember_me = forms.BooleanField(label = 'Remember me ', initial=False,  required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    
    # implementing google rechapcha.
    captcha = ReCaptchaField( widget=ReCaptchaV2Checkbox) 
    
    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']    
    
    
    # Taking charge oif default method of Django to give more interactiveess.
    def clean(self, *args, **kwargs): 
        captcha = self.cleaned_data.get('captcha')       
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        # to give more userfriendly experience.
        if not captcha:
            raise forms.ValidationError("Captcha Check required")
            
        if email and password:
            #check email verification                      
            email_qs = User.objects.filter(email=email)            
            if not email_qs.exists():
                # if no user with this email, user will get message.
                raise forms.ValidationError("The user does not exist")
            else:
                try:
                    '''
                    If have user but email is not verified will send verification emaila again, as
                    previous mail can be lost.
                    will see warning message also.
                    '''
                    ver_email = User.objects.filter(email=email, email_verified=False).first() 
                    subject = 'Email Verification Required!'  
                    current_site = Site.objects.get_current()  
                    message = render_to_string('emails/account_activation_email.html', {
                        'user': ver_email,                    
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(ver_email.pk)),
                        'token': account_activation_token.make_token(ver_email),                        
                    })                   
                    ver_email.email_user(subject, '', html_message=message)                   
                    messages.warning(self.request, f'Email is not verified, your need to verify the email. An email verification link has been sent to your mailbox {email}')                   
                except Exception as e:    
                    '''
                    If email verified but not activated yet(It is happem=nd for expert type of user.)
                    user will get curtesy mail and message.
                    '''                          
                    is_active_qs = User.objects.filter(email=email, is_active=False).first()                
                    if is_active_qs:  
                        if is_active_qs.is_expert or is_active_qs.is_marine:
                            raise forms.ValidationError("Your account is not activated by site admin, please wait for approval!")     
                        else:             
                            subject = 'Account activation required!'  
                            current_site = Site.objects.get_current()  
                            message = render_to_string('emails/account_activation_email.html', {
                                'user': is_active_qs,                    
                                'domain': current_site.domain,
                                'uid': urlsafe_base64_encode(force_bytes(is_active_qs.pk)),
                                'token': account_activation_token.make_token(is_active_qs),                        
                            })                 
                            
                            is_active_qs.email_user(subject, '', html_message=message)                   
                            raise forms.ValidationError(f'Account is not active, your need to activate your account before login. An account activation link has been sent to your mailbox {email}')                
                    else:
                        '''
                        if no problem user will be autheticated.
                        request args in below function essential for axes to control failed login and blocking.
                        '''
                        user = authenticate(request=self.request,email=email, password=password)  
                        if not user:
                            raise forms.ValidationError("Incorrect password. Please try again!")             
                                    
        return super(LoginForm, self).clean(*args, **kwargs)
    
