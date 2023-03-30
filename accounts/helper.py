from django.core.exceptions import PermissionDenied
from evaluation.models import *
from accounts.models import *
from django.contrib.auth.validators import UnicodeUsernameValidator, ASCIIUsernameValidator
from django.utils.translation import gettext_lazy as _

from django.core.mail import mail_admins, send_mail, send_mass_mail
class CustomsernameValidator(UnicodeUsernameValidator, ASCIIUsernameValidator):
    regex = r'^[\w.]+\Z'
    
    message = _(
        'Enter a valid username. This value may contain only letters, '
        'numbers'
    )

# The function is abandoned and no where using currently.
def check_type(request, slug):   
    try:
        curnt_user_type_slug = request.user.usertype.slug
    except Exception as e:        
        curnt_user_type_slug = None     
    if curnt_user_type_slug == slug or request.user.is_staff or request.user.is_superuser:
        pass
    else:
        raise PermissionDenied
    
def send_admin_mail(subject, message):
    from .models import User
    admins = User.objects.filter(is_staff=True, is_active = True)    
    email_recipent = []
    for admin in admins:         
        email_recipent.append(admin.email)            
    send_all_email = [(subject, message, settings.DEFAULT_FROM_EMAIL, [e]) for e in email_recipent]
    send_mass_mail((send_all_email), fail_silently=False) 
    

    