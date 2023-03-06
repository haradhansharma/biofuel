from crm.forms import SubscriberForm

        
def get_pending_sugestion():
    from evaluation.models import Suggestions
    
    count = Suggestions.objects.filter(comitted =False).count()
    
    return count
        


def site_info():
    from .models import ExSite
    site = ExSite.on_site.get()   
    site_info = {
        'name' : site.site.name,
        'domain' : site.site.domain, 
        'canonical' : site.site.domain,
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
        'topic' : 'Green Fuel',
        'type' : 'Fuel Validation Platform',
        'robots' : "index, follow"        
    }
    
    return site_info


    

def comon_doc(request):
   
    load_template = list(filter(None, request.path.split('/')))
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
            'segment' : load_template,
            'subscription_form' : SubscriberForm(),
            'sugestion_no_comited' : get_pending_sugestion()
            
    }
    
