from crm.forms import SubscriberForm
from navigation.menu import (
    header_menus,
    account_menus,
    dashboard_menu
)
from django.db.models import F, Count        
from django.core.cache import cache
from .models import ExSite


def site_info():
    SITE_INFO_CACHE_KEY = 'site_info'    
    site_info = cache.get(SITE_INFO_CACHE_KEY)
    
    if site_info is not None:
        return site_info
    
    site = ExSite.on_site.select_related('site').get()
    
    site_info = {
        'name': site.site.name,
        'domain': site.site.domain,    
        'meta_name': site.site_meta,
        'description': site.site_description,
        'tag': site.site_meta_tag,
        'favicon': site.site_favicon.url,
        'mask_icon': site.mask_icon.url,
        'logo': site.site_logo.url,
        'slogan': site.slogan,
        'og_image': site.og_image.url,
        'phone': site.phone,
        'email': site.email,
        'location': site.location,
        'facebook_link': site.facebook_link,
        'twitter_link': site.twitter_link,
        'linkedin_link': site.linkedin_link,
        'qualified_ans_range' : site.qualified_ans_range,
        'topic': 'Green Fuel',
        'type': 'Fuel Validation Platform',
        'robots': 'index, follow',
        'author' : 'gf-vp Team'
    }
    
    cache.set(SITE_INFO_CACHE_KEY, site_info, timeout=3600)

    return site_info


def get_pending_sugestion():
    from evaluation.models import Suggestions
    
    # First, check if the count is already cached
    count = cache.get('pending_suggestion_count')
    if count is None:
        # If not, fetch the count from the database and cache it for future use
        count = Suggestions.objects.filter(comitted=False).aggregate(count=Count('id'))['count']
        cache.set('pending_suggestion_count', count)

    return count


def comon_doc(request):   
 
    text = {
        'user_congrets': f"Hi , {request.user.username}",
        'signup':' Sign Up',
        'going_to_be' : 'Going to be ',
        'not': 'If you are not ',
        'restart' : 'Click to Restart',
        'type' : 'Type',
        'expert_in' : 'Experts In',
        'have_account': 'Already have an account?',
        'signin' : 'Sign In',
        'credentials' : 'Add your credentials',
        'forget_pass' : 'Forget Password?',
        'not_registered' : 'Not registered?',
        'create_account' : 'Create Account',
        'reset_pass' : 'Reset Password Here!',
        'email_sent' : 'Email Sent',
        'check_inbox' : 'Check Your Inbox',
        'reset_done' : 'Password Reset Done',
        'set_a_new' : 'Set a New Password',
        'enter_new' : 'Enter New Password',
        'set_new' : 'Set New Password',
        'reset_complete' : 'Passowrd Reset Complete',
        'error404' : 'Error 404',
        'error403' : 'Error 403',       
    }
    

    return {   
            'site_info': site_info(),
            'text': text,     
            'subscription_form' : SubscriberForm(),
            'sugestion_no_comited' : get_pending_sugestion(),
            'header_menus' : header_menus(request),
            'account_menus' : account_menus(request),
            'dashboard_menu' : dashboard_menu(request), 
       
            
    }
    
