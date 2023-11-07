from django import forms
from django.contrib.auth.forms import (
    UserCreationForm as UserCreationFormDjango,
    UserChangeForm as UserChangeFormDjango,
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
    PasswordChangeForm,
)
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .models import User, NotificationSettings
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.contrib.auth import authenticate
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin
from django.core.exceptions import ValidationError
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible, ReCaptchaV2Checkbox



class UserCreationForm(UserCreationFormDjango):
    """
    Custom User Creation Form that extends the default Django UserCreationForm in Admin.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the UserCreationForm instance.
        """
        super(UserCreationForm, self).__init__(*args, **kwargs)

    UserAdmin.add_form = UserCreationFormDjango
    # Update the UserAdmin's add_form to use the Django's default UserCreationForm.

    UserAdmin.add_fieldsets = ((None, {
        'classes': ('wide',),
        'fields': ('usertype', 'email', 'phone', 'username', 'password1', 'password2', 'term_agree', 'experts_in',)
    }),)
    # Update the UserAdmin's add_fieldsets to include additional fields and customize its appearance.

    class Meta:
        """
        Metadata class for the UserCreationForm.
        """
        model = get_user_model()
        fields = '__all__'
        # Include all fields from the user model in the form.

 
class UserCreationFormFront(UserCreationFormDjango):
    """
    Custom User Creation Form for the frontend registration page.
    """

    # Custom fields with HTML attributes
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(attrs={
            "placeholder": "Username",
            "class": "form-control",
            'hx-post': reverse_lazy('accounts:check_username'),
            'hx-target': '#username_error',
            'hx-trigger': 'keyup[target.value.length > 3]'
        })
    )
    email = forms.EmailField(
        label='E-mail Address',
        widget=forms.EmailInput(attrs={
            "placeholder": "Email",
            "class": "form-control",
            'hx-post': reverse_lazy('accounts:check_email'),
            'hx-target': '#email_error',
            'hx-trigger': 'keyup[target.value.length > 3]'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={"placeholder": "Password check", "class": "form-control"})
    )
    term_agree = forms.BooleanField(
        label='Agree Our',
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    newsletter_subscription = forms.BooleanField(
        label='Subscribe to our newsletter',
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"})
    )
    
    # Google reCAPTCHA field
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        """
        Metadata class for the UserCreationFormFront.
        """
        model = get_user_model()
        fields = (
            'orgonization', 'username', 'email', 'password1', 'password2',
            'term_agree', 'newsletter_subscription', 'usertype', 'experts_in', 'is_public'
        )
        
        # Widgets for additional form fields
        widgets = {
            'usertype': forms.Select(attrs={
                'class': 'form-select',
                'aria-label': 'usertype',
                'hx-post': "/check_type_to_get_expert/",
                'hx-trigger': "change",
                'hx-target': "#hx",
                'hx-swap': "innerHTML",
             
            }), 
            'experts_in': forms.Select(attrs={'class': 'form-select', 'aria-label': 'experts_in'}),
            'orgonization': forms.TextInput(attrs={
                'placeholder': 'My Organization',
                'class': 'form-control',
                'aria-label': 'organization'
            }),
            'is_public': forms.CheckboxInput(attrs={"class": "form-check-input"})
        }

    def clean_username(self):
        """
        Validate username to disallow spaces.
        """
        data = self.cleaned_data.get('username')
        if " " in data:
            raise ValidationError("Spaces in username are not allowed!")
        return data
    
    def clean_experts_in(self):
        """
        Validate experts_in field based on the user type.
        """
        user_type = self.cleaned_data.get('usertype')
        data = self.cleaned_data.get('experts_in')
        if user_type.is_expert and not data:
            raise ValidationError("Experts In field is required for expert users.")
        return data
    
    def clean(self, *args, **kwargs):
        """
        Custom clean method to handle various validations and email verifications.
        """
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        
        # Check if email, password, or username is provided
        if email or password or username:            
            # Check email verification                      
            email_qs = User.objects.filter(email=email)            
            if not email_qs.exists():
                # Continue to the registration process
                pass
            else:
                '''
                if user already registered and not verified the email,
                system will send activation mail again.
                as previous activation mail may be invalid or loss by user.
                '''    
                
                ver_email = email_qs.filter(email_verified=False)                
                
                if ver_email.exists():
                    # if Email not verified                    
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
                                                               
                    is_active_qs = email_qs.filter(is_active=False).first()                
                    if is_active_qs:  
                        if is_active_qs.is_expert or is_active_qs.is_marine:
                            # Expert and manire user need manual activation by admin
                            raise forms.ValidationError("You have an account already with this email. But account is not activated by site admin, please wait for approval!")                              
                        else:    
                            # for other non verified email.         
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


    
    

class UserChangeForm(UserChangeFormDjango):
    '''
    Inheriting dafault django form to give the facility to edit self account data.
    Currently it is being used in dashboard>>setting and dashboard>>password change form.
    '''
    class Meta:
        model = get_user_model()
        fields = '__all__'
    widgets = {                              
            'email': forms.EmailInput(attrs={ 'class':'form-control', 'aria-label':'email' }),
        }
        

class LoginForm(AuthenticationForm):
    
    """
    Custom login form with extended fields, custom validations, and reCAPTCHA integration.
    """
    
    
    # Customizing the default Django form fields and adding HTML attributes
    username = forms.CharField(widget=forms.TextInput(attrs={ "class": "form-control" }))    
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))  
    
    
    # Option to remember the user's login for 30 days acording to the site settings
    remember_me = forms.BooleanField(label = 'Remember me ', initial=False,  required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))
    
    # Implementing Google reCAPTCHA
    captcha = ReCaptchaField( widget=ReCaptchaV2Checkbox) 
    
    class Meta:
        """
        Meta class to define the fields and widgets used in the form.
        """
        model = get_user_model()
        fields = ['username', 'password', 'remember_me']    
    
    

    def clean(self, *args, **kwargs): 
        """
        Custom validation and checks for email verification, account activation, and password.
        """
        captcha = self.cleaned_data.get('captcha')       
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        # Check if the captcha was completed
        if not captcha:
            raise forms.ValidationError("Captcha Check required!")
            
        if email and password:
            # Check if the email exists in the system                  
            email_qs = User.objects.filter(email=email)            
            if not email_qs.exists():
                # If no user with this email, show a message
                raise forms.ValidationError("The user does not exist")
            else:
                try:
                    # Handle cases where the email is not verified
                    '''
                    If have user but email is not verified will send verification emaila again, as
                    previous mail can be lost.
                    will see warning message also.
                    '''
                    ver_email = email_qs.filter(email_verified=False).first() 
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
                    If email verified but not activated yet(It is happned for expert and marine type of user.)
                    user will get mail and message.
                    '''                          
                    is_active_qs = email_qs.filter(is_active=False).first()                
                    if is_active_qs:                          
                        if is_active_qs.is_expert or is_active_qs.is_marine:
                            # Handle cases where the email verified but not activated
                            raise forms.ValidationError("Your account is not activated by site admin, please wait for approval!")     
                        else:    
                            # Send activation email again         
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
                        # Authenticate the user using email and password
                        '''
                        if no problem user will be autheticated.
                        request args in below function essential for axes to control failed login and blocking.
                        '''
                        user = authenticate(request=self.request,email=email, password=password)  
                        if not user:
                            # Invalid password, show an error message
                            raise forms.ValidationError("Incorrect password. Please try again!")             
                                    
        return super(LoginForm, self).clean(*args, **kwargs)
    
    
class NotificationSettingsForm(forms.ModelForm):
    class Meta:
        model = NotificationSettings
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        print(kwargs)
        super(NotificationSettingsForm, self).__init__(*args, **kwargs)
        user = kwargs['instance'].user
        print(user.is_consumer)
        if not user.is_consumer or user.is_staff or user.is_superuser:
            self.fields.pop('new_fuel_notifications')
        # Define the CSS class you want to add to all fields
        css_class = 'form-control'

        # Iterate through all fields in the form
        for field_name, field in self.fields.items():
                
            if isinstance(field, forms.BooleanField):
                # This field is a BooleanField
                field.widget.attrs['class'] = 'form-check-input'
            else:
                # Add the class attribute to other fields
                field.widget.attrs['class'] = css_class
               
    
