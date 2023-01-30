from django.core.exceptions import PermissionDenied
from evaluation.models import *
from accounts.models import *




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
    

    