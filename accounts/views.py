from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from urllib.parse import urlparse
from django.http import HttpResponse, HttpResponseRedirect
from doc.models import ExSite
from evaluation.models import (
    Evaluator 
    )
from .models import *
from django.urls import reverse_lazy
from gfvp import null_session
from django.shortcuts import render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.views import LoginView
from crm.models import *
from crm.views import get_location_info
from evaluation.helper import (
    get_all_questions,
    LabelWiseData,
    get_all_reports_with_last_answer
    ) 
from doc.doc_processor import site_info
from django.db.models import Q
from accounts.decorators import producer_required, consumer_required, expert_or_producer_requried
import logging
log =  logging.getLogger('log')

from accounts.decorators import (
    expert_required
)

from accounts.helper import send_admin_mail

'''
Inheriting default loginview of Django and customizing behavior.
'''
class CustomLoginView(LoginView):
    
    """
    Customized login view based on Django's LoginView.

    Inherits from Django's built-in LoginView and customizes its behavior:
    - Uses a custom login form (LoginForm).
    - Sets a custom URL for redirection after successful login.
    - Handles the 'remember me' functionality to control session duration.

    Attributes:
        form_class (LoginForm): The custom login form to be used.
        next_page (str): The URL to redirect to after successful login.

    Methods:
        form_valid(form): Overridden method to handle form validation on login.
        get_context_data(**kwargs): Overridden method to provide additional context data.
    """
    
    #To avoid circular reference it is need to import here
    from .forms import LoginForm
    
    # Overwrite form class to use custom LoginForm
    form_class = LoginForm 
    
    # Custom URL for redirection after login
    next_page = ''
    #taking control over default of Django  
    def form_valid(self, form): 
        
        """
        Handle form validation for login.

        This method is called when the form is valid upon submission.
        Customizes the session behavior based on 'remember me' checkbox.

        Args:
            form (LoginForm): The validated login form.

        Returns:
            HttpResponse: The response after processing the login form.
        """
        
        # Set custom after-login URL
        self.next_page = reverse_lazy('accounts:user_link')       
            
        log.info(f'Login page validating by_____________ {self.request.user}')
        
        #rememberme section        
        remember_me = form.cleaned_data.get('remember_me')     
        if not remember_me:
            # Set session expiry to 0 seconds, closing the session after browser is closed.
            self.request.session.set_expiry(0)
            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True  
        return super(CustomLoginView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        """
        Retrieve additional context data for the login view.

        This method is called to fetch and provide extra context data for rendering the view.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing context data for rendering the view.
        """
        
        log.info(f'Login accessed by_____________ {self.request.user}')
        
        
        context = super().get_context_data(**kwargs)
        
        # Generate meta data for the view
        meta_data = site_info()    
        meta_data['title'] = 'User Login'    
        meta_data['description'] = ("The Log In page of gf-vp.com is designed to provide secure access to the "
                                   "user's account. Users can easily log in to their account with their email "
                                   "and password.")
        meta_data['tag'] = 'login, gf-vp.com'
        meta_data['robots'] = 'noindex, nofollow'        
        context.update({
            'site_info' : meta_data                
        })
        return context




def signup(request, slug=None):  
    
    
    """
    View function for user signup.

    This view handles the signup procedure for different user types and experts' subtypes.
    The process involves segregating users based on their selected user type or expert subtype.
    Users who have already selected a user type during their session are directed to the signup form.
    If anyone attempts to signup without selecting a user type, they are redirected to choose one.
    Expert users only need to select the "Expert" user type during signup.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered signup page or redirection to appropriate pages.
    """    
     
    # Importing UserCreationFormFront to avoid circular reference.
    from .forms import UserCreationFormFront
    
    '''
    =====
    Part of user type segrigation 
    =====
    '''
    
    log.info(f'signup page accessed by_____________ {request.user}') 
    
    if slug == None or slug == '':
        messages.error(request, 'Should have user types key in the url! Select one from below!')
        return HttpResponseRedirect(reverse('home:home') + '#register')  
    else:
        slugs = UserType.objects.values_list('slug', flat=True)
        if slug in slugs:
            pass
        else:
            messages.error(request, 'Wrong user type key given! Click on below to provide correct one!')
            return HttpResponseRedirect(reverse('home:home') + '#register')  
            
    
            

    # # User type segregation based on session.
    # if 'interested_in' not in request.session:
    #     request.session['interested_in'] = None     
          
    # if request.session['interested_in'] == None:    
    #     #Ensure Selection of User Type based on session
    #     referer = urlparse(request.META.get('HTTP_REFERER')).path 
    #     try:       
    #         type_path = reverse('types', args=[str(request.session['interested_in'])] )
    #     except Exception as e:            
    #         type_path = None           
    #     if referer != type_path:  
    #         messages.warning(request, f'Select your business type to register!')             
    #         # user type selected facility in the home page so we will forwared user there     
    #         return HttpResponseRedirect(reverse('home:home') + '#register')     
 
    # Session-controlled interactivity in frontend.
    slug_of_expart = UserType.objects.get(is_expert = True).slug   
    
    if slug_of_expart == slug:    
        hidden = ''
    else:
        hidden = 'hidden' 
        
              
        
    if request.method == 'POST':        
        #preparation to send site data to the mail template
        current_site = get_current_site(request)
        
        #customized form to take user data
        form = UserCreationFormFront(request.POST)
        
        if form.is_valid():           
            new_user = form.save()      
            #ensure user inactive to verify email.              
            new_user.is_active = False
            new_user.save()   
            subject = f'{current_site.domain}-Account activation required!' 
            message = render_to_string('emails/account_activation_email.html', {
                # Parameters for the mail template.
                # Activation link is built in the template.
                'user': new_user,                    
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),                
            })
            
            new_user.email_user(subject, '', html_message=message)            
            messages.success(request, 'Please confirm your email to complete registration.') 
            # Redirect after successful submission to avoid user confusion.
            return HttpResponseRedirect(reverse_lazy('login'))          
            
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)   
            return HttpResponseRedirect(reverse_lazy('accounts:signup'), args=[str(slug)])          
                     
    else:
        
        '''
        We will show users in which usertype the are going to register for.
        if they are not seeing appropriate to them then they can re start by clcking restart button(implemented from template)
        will ensure they have selected their desired type.
        otherwise they will be forwarded to home page to progress as per system mentioned in the starting of the function.
        '''      
        
                  
        try:
            usertype = UserType.objects.get(slug = slug)   
        except Exception as e:            
            # usertype = None  
            messages.warning(request, f'Select your business type to register!') 
            
            # user type selected facility in the home page so we will forwared user there     
            return HttpResponseRedirect(reverse('home:home') + '#register')  
        
        
        # Interacting behind the scenes.
        # By default, site is set to have all checkboxes ticked for Term agree and newsletter subscription and user type.
        initial_dict = {
            'usertype': usertype,
            'newsletter_subscription' : True,
            'term_agree' : True           
        }     
        
        form = UserCreationFormFront(initial = initial_dict)
        
        
    # Meta data.
    meta_data = site_info()    
    meta_data['title'] = 'Sign Up'
    meta_data['description'] = f"The Sign Up page of the gf-vp.com provides users with the ability to create a new account. This page allows users to enter their email address, username, and password."
    meta_data['tag'] = 'signup, gf-vp.com'
    meta_data['robots'] = 'noindex, nofollow'
        
    context = {
        'hidden' : hidden,
        'slug' : slug,
        'form': form,
        'usertype': usertype,
        'site_info' : meta_data           
    }
    return render(request, 'registration/signup.html', context = context)


def activate(request, uidb64, token):
    
    """
    Activates a user's account using the provided activation link.
    If user not expert and not in expert types account will activate autometically
    Expert Type user need admin intervention for account activation    
    Creating LEAD
    Creating Newsletter subscription

    Args:
        request (HttpRequest): The HTTP request object.
        uidb64 (str): The base64-encoded user ID.
        token (str): The activation token.

    Returns:
        HttpResponseRedirect: Redirects to the appropriate view based on the activation result.
    """
    
    # Preparation to pass data to the site
    current_site = get_current_site(request)
    
    # Preparation to check activation URL
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        # If the activation link is valid, mark the account as email verified
        user.email_verified = True        
        
        if user.is_expert or user.is_marine:    
            # If user is an expert or marine, activate manually by site admin        
            user.is_active = False
            subject = 'Please Wait for approval'               
            message = render_to_string('emails/regi_mail_to_expert.html', {
                'user': user,                    
                'domain': current_site.domain,                            
            })
            user.email_user(subject, '', html_message=message)            
            messages.success(request, 'Email verified, please wait for approval!')
        else:
            # If email verified and user is not an expert, activate the account
            user.is_active = True
            subject = 'Account has been Activated!' 
            message = render_to_string('emails/account_activated.html', {
                'user': user,                    
                'domain': current_site.domain,
                'exsite': ExSite.on_site.get(),   
                'login' : request.build_absolute_uri('/accounts/login/')        
            })
            # User will recive activation mail.
            user.email_user(subject, '', html_message=message)   
            messages.success(request, ('Your account have been confirmed.'))                
            
                
            
        # Save user after checking user type for different approval policy
        user.save()   
        
        '''
        CREATING LEAD 
        '''
        # If email verified and user ticked to receive the newsletter, save the user to the CRM
        location_info = get_location_info(request)
        location_info = get_location_info(request)
        city =  location_info.get('city') 
        country_code = location_info.get('country')
        country = country_code
        full_name = user.get_full_name()
        
        '''
        CREATING NEWSLETTER SUBSCRIPTION
        '''
        
        # If user ticked to get our newsletter during signup process
        # We will check the email already have in our crm or not
        # If already exists then whatever his subscription status is we will make the status to True as email is verified here and ticked on the subscription
        # If not exists we will create a lead having the user data.
        if user.newsletter_subscription:
            log.info(f'Creating lead for {user.email} ')
            try:
                lead = Lead.objects.get(email_address = user.email)                             
            except Exception as e:                
                lead = None
                
            if lead is not None:
                lead.update(subscribed=True)                
            else:
                Lead.objects.create(lead = full_name if full_name else user.username, email_address=user.email,city=city,country=country,subscribed=True)
        return HttpResponseRedirect(reverse_lazy('login'))
    else:
        messages.warning(request, ('Activation link is invalid!'))
        return HttpResponseRedirect(reverse_lazy('home:home'))
    


@login_required 
def userpage(request):  
    """
    This view function displays the user's profile page, showing information about their reports and activities.
    
    Args:
        request (HttpRequest): The request object from the client.
    
    Returns:
        HttpResponse: The rendered user profile page with relevant data.
    """
    
    log.info(f'Userpage accessed by_____________ {request.user}')
    
    # Clear the session data to ensure a clean state when the user logs in.
    null_session(request)   #This is essential where user loggedin    
 
 
    
    user = request.user
    
    report_slug = request.GET.get('slug')
    
    if report_slug:
        try:
            # Retrieve a specific report using the provided slug.
            last_reports = Evaluator.objects.get(slug = report_slug)
        except Exception as e:          
            last_reports = None 
    else:        
        try:
            # Retrieve the most recent report created by the user.
            last_reports = Evaluator.objects.filter(creator = user).order_by('-create_date').first()  
        except Exception as e:            
            last_reports = None
    
            
    if last_reports is not None: 
        # Generate label-wise data from the last report.
        label_data = LabelWiseData(last_reports)    
        
        gretings = f'The summary of the report number {last_reports.id} genarated by {user.username}!'        
        
        # Calculate various statistics based on label data.
        ans_ques = len(label_data.answered_question_id_list)
        dont_know_ans = ans_ques - label_data.total_positive_answer - label_data.total_nagetive_answer
        pos_ans = label_data.total_positive_answer
        positive_percent = label_data.overview_green
        dont_know_percent = label_data.overview_grey
         
        
        # Explanation about the importance of having a parent question set for evaluation.
        '''
        **** As mentioned on several pages, a parent question set is mandatory for the evaluation procedure. ****
        This is because if a user starts an evaluation but doesn't submit any answers to the questions,
        then the system will forward them to the first parent question. Otherwise, the system will redirect to the last question when editing the report.
        '''
        
        try:    
            # Retrieve the first parent question for the evaluation.         
            first_of_parent = get_all_questions().filter(is_door=True).order_by('sort_order').first()
        except:
            # Display a warning message if there is an issue with the procedure settings.
            messages.warning(request,'There is something wrong in procedure setting by site admin please try again latter!')
            return HttpResponseRedirect(reverse('evaluation:evaluation2')) 
          
        # Get all reports with the last answer related to the first parent question.
        reports = get_all_reports_with_last_answer(request, first_of_parent)
        
        # Paginate the reports for display.
        page = request.GET.get('page', 1)
        paginator = Paginator(reports, 10)
        try:
            reports = paginator.page(page)
        except PageNotAnInteger:
            reports = paginator.page(1)
        except EmptyPage:
            reports = paginator.page(paginator.num_pages)
            
        # Construct the URL for a button linked to the last report.
        button = reverse('evaluation:nreport', args=[last_reports.slug])        
        
        # Prepare the context for rendering the user profile page.
        context = {
            'donotshow' : 'no',
            'refferer_path' : urlparse(request.META.get('HTTP_REFERER')).path,            
            'gretings': gretings,
            'button': button,
            'ans_ques': ans_ques,
            'dont_know_ans': dont_know_ans,
            'pos_ans': pos_ans,
            'last_reports' : last_reports,
            'positive_percent': str("%.2f" % positive_percent) + '%',
            'dont_know_percent': str("%.2f" % dont_know_percent) + '%',
            'reports': reports,       
            'last_report_button_text' : 'Get Last Report',
            'username' : user.username,   
  
            
        }
    else:
        
        # If no reports have been created by the user, display relevant links.        
        gretings = 'Below links will help you to explore the site!'        
        
        context = {
            'gretings': gretings,
            'last_reports' : last_reports,
            'accounts_seting' : 'Accounts Settings',
            'dashboard' : 'Dashboard',
            'change_pass' : 'Change Password',
            'homepage' : 'Home Page',
        
        } 
        
    # Prepare meta data for the page.
    meta_data = site_info()    
    meta_data['title'] = user.username
    meta_data['description'] = (f"This is the personalized user profile page for {user.username}. " 
                                "Here, registerd user can view his information and created reports. " 
                                "Also Can go to the profiel setting page.")
    meta_data['tag'] = 'user profile, gf-vp.com'
    meta_data['robots'] = 'noindex, nofollow'
    meta_data['og_image'] = user.usertype.icon.url 
    
   
    # Update the context with meta data.
    context.update(
        {
            'site_info' : meta_data,            
        }
    )
        
    return render(request, 'registration/userpage.html', context = context)


def check_username(request):
    
    """
    Check the availability and validity of a username in a signup form.

    This function takes a POST request containing a 'username' parameter
    and checks if the provided username is valid and available for registration.

    Args:
        request (HttpRequest): A POST request containing the 'username' parameter.

    Returns:
        HttpResponse: A response indicating whether the username is valid and available.
            - If the username contains spaces, returns a danger message.
            - If the username already exists in the User model, returns a danger message.
            - If the username is valid and available, returns a success message.
    """
    # Retrieve the username from the POST request
    username = request.POST.get('username')
    
    # Check for spaces in the username
    if " " in username:
        return HttpResponse(' <span class="text-danger"> Space Not allowed! </span>') 
    
    # Check if the username already exists in the User model
    if User.objects.filter(username = username).exists():
        return HttpResponse(' <span class="text-danger"> This username already exists! </span>') 
    else:
        return HttpResponse('<span class="text-success">This username available!</span>')    

    
def check_email(request):
    """
    Checks the validity and availability of an email address provided in a sign-up form.
    
    This function takes a POST request containing an email address from a sign-up form
    and performs the following checks:
    
    1. Validates the email format using Django's `validate_email` function.
    2. Checks if the email address already exists in the User model.
    
    If the email is valid and not already taken, it returns a success message. If the
    email is invalid, already taken, or an exception occurs during validation, it returns
    an appropriate error message.
    
    Args:
        request (HttpRequest): The HTTP request containing the email in the POST data.
        
    Returns:
        HttpResponse: A response indicating the validity and availability of the email.
    """
    
    from django.core.validators import validate_email
    email = request.POST.get('email')    
    try: 
        validate_email(email)   
        if User.objects.filter(email = email).exists():
            return HttpResponse(' <span class="text-danger"> This email already exists! </span>')
        else:
            return HttpResponse('<span class="text-success">This email available!</span>')
    except:
        return HttpResponse('<span class="text-danger">Type a valid email address!</span>')
    
@login_required
@producer_required
@expert_required
@expert_or_producer_requried
def partner_service(request, pk):
    """
    Display the personalized service page for a partner user.
    
    This view displays the personalized service page for a visiting partner user. It retrieves the necessary information
    such as next activities and selected activities to be displayed on the page. It also handles visibility permissions
    based on the user's role (expert, staff, superuser). Additionally, it generates meta data for SEO purposes.
    
    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the visiting user.
        
    Returns:
        HttpResponse: Rendered HTML template displaying the service page. 
    """
    
    log.info(f'Partner service page accessed by_____________ {request.user}')
    
    
    # To avoid circular reference
    from evaluation.models import NextActivities
    
    # Get the visiting user based on the provided primary key (pk).
    visiting_user = get_object_or_404(User, pk=pk, is_active = True, is_public = True)
    
    # Get the currently logged-in user.
    current_user = request.user    
    
    # Retrieve all next activities with prefetch for related 'quotnextactivity'.
    next_activities = NextActivities.objects.filter(is_active = True).prefetch_related('quotnextactivity')
    
    # Get the selected activities of the visiting user.
    visiting_users_selecetd = visiting_user.selected_activities
    
    # Create a list of next activities from the selected activities.
    na_in_una = [na.next_activity for na in visiting_user.selected_activities] if visiting_users_selecetd else None
    
    # Notify the admin if there are no next activities and the current user is an expert.
    if not next_activities.exists() and current_user.is_expert:
        subject = f'Validation partner are visiting service page but no default service'
        message = 'Hello Admin,\n\nThis is an important notification that vlidation partner are visiting the service page there is no Next Activities to select by then. Please add some next activities.\n\nBest regards,\nAdmin Team'            
        send_admin_mail(subject, message)
    
    # Determine if the visiting user's role allows visibility of certain blocks.  
    if current_user.is_expert or current_user.is_staff or current_user.is_superuser:
        block_visible = True
    else:
        block_visible = False        
    
     # Create a dictionary containing the context data to be passed to the template.
    context ={
        'visiting_user' : visiting_user,
        'current_user' : current_user,
        'next_activities' : next_activities,
        'na_in_una' : na_in_una,
        'block_visible' : block_visible        
    }    
    
    # Generate meta data for SEO and page information.
    meta_data = site_info()    
    meta_data['title'] = f'Service of {current_user.username}'
    meta_data['description'] = f"This is the personalized Service page for {current_user.username}. Here, registerd user can view his information and manage services."
    meta_data['tag'] = 'user profile, gf-vp.com'
    meta_data['robots'] = 'noindex, nofollow'
    meta_data['og_image'] = current_user.usertype.icon.url 
    
    # Update the context with the generated meta data.    
    context.update(
        {
            'site_info' : meta_data,            
        }
    )
    
    # Render the template with the provided context.
    return render(request, 'registration/partner_service.html', context = context)


@login_required
@expert_required   
def commit_service(request, user_id, na_id):
    """
    View function to handle committing a service by a user.

    This view performs the following steps:
    1. Check if the user is logged in and has the necessary permissions.
    2. Fetches the necessary data related to next activities and users.
    3. Verifies the user's authenticity and the validity of the next activity.
    4. Creates a record of the user committing the next activity if not already present.
    5. Prepares data for rendering the commit service page.

    Args:
        request (HttpRequest): The request object.
        user_id (str): The ID of the user committing the service.
        na_id (str): The ID of the next activity being committed.

    Returns:
        HttpResponse: A response containing the rendered commit service page or an error message.

    Raises:
        HttpResponse: If the user is not logged in, does not have the necessary permissions,
                      or if any unethical operation is detected.
    """
    context = {}
    current_user = request.user  
    
    # Check if user is not logged in
    if user_id == 'None':        
        return HttpResponse('You have not logged in and it is unethical operation!')
    else:
        from evaluation.models import NextActivities     
        next_activities = NextActivities.objects.filter(is_active = True).prefetch_related('quotnextactivity')
        
        # Check if the current user's ID matches the given user_id
        if int(user_id) != current_user.id:
            return HttpResponse('It is unethical operation, User does not match!')
            
        try:
            visiting_user = User.objects.get(id = int(user_id), is_active = True) 
        except:
            return HttpResponse('It is unethical operation! No user found!')
        
        try:
            na = next_activities.get(id = int(na_id))
        except:
            return HttpResponse('It is unethical operation! No Next Activities found!')
        
        una = UsersNextActivity.objects.filter(user = visiting_user)
        na_in_una = [na.next_activity for na in una]
        
        # Create a record of the user committing the next activity if not present
        if na not in na_in_una:
            UsersNextActivity.objects.create(next_activity = na, user = visiting_user)        
         
        # Check user's permissions to set block_visible flag 
        if current_user.is_expert or current_user.is_staff or current_user.is_superuser:
            block_visible = True
        else:
            block_visible = False
        
        data = {
            'visiting_user' : visiting_user,
            'current_user' : current_user,
            'next_activities' : next_activities,
            'na_in_una' : [na.next_activity for na in una.all()],
            'block_visible' : block_visible
            
        }
        
        context.update(data)   
    
    
    return render(request, 'registration/commit_service.html', context = context)



@login_required
@expert_required   
def delete_service(request, user_id, na_id):
    """
    This view function allows an expert user to delete a specific Next Activity
    associated with a visiting user.

    Args:
        request (HttpRequest): The HTTP request object.
        user_id (str): The ID of the visiting user.
        na_id (str): The ID of the Next Activity to be deleted.

    Returns:
        HttpResponse: A rendered HTML response displaying the result of the operation.
    """
    
    context = {}
    current_user = request.user
       
    if user_id == 'None':        
        return HttpResponse('You have not logged in and it is unethical operation!')
    else:
        # To avoid circular reference
        from evaluation.models import NextActivities    
        
        # Retrieve the list of active Next Activities and their related quotnextactivity objects
        next_activities = NextActivities.objects.filter(is_active = True).prefetch_related('quotnextactivity')
        
        # Check if the current user has the permission to delete Next Activities
        if int(user_id) != current_user.id:
            return HttpResponse('It is unethical operation, User does not match!')
            
        try:
            visiting_user = User.objects.get(id = int(user_id), is_active = True)
        except:
            return HttpResponse('It is unethical operation! No user found!')
        
         # Fetch all Next Activities associated with the visiting user
        una = UsersNextActivity.objects.filter(user = visiting_user)
        
        try:
            # Attempt to retrieve the target Next Activity to be deleted
            target_una = una.get(id = int(na_id), user = visiting_user)
        except:
            return HttpResponse('It is unethical operation! No Next Activities found!')
        
        # Delete the target Next Activity
        target_una.delete()
        
        # Determine if the block should be visible to the user based on their role
        if current_user.is_expert or current_user.is_staff or current_user.is_superuser:
            block_visible = True
        else:
            block_visible = False
                
        # Prepare the data to be sent to the template
        data = {
            'visiting_user' : visiting_user,
            'current_user' : current_user,
            'next_activities' : next_activities,
            'na_in_una' : [na.next_activity for na in una.all()],
            'block_visible' : block_visible            
        }
        
        # Update the context with the prepared data
        context.update(data)
    
    
    # Render the template and return the HTML response
    return render(request, 'registration/commit_service.html', context = context)


@login_required
@consumer_required
def producer_fuels(request, pk):
    
    # Get the visiting user based on the provided primary key (pk).
    visiting_user = get_object_or_404(User, pk=pk, is_active = True, is_public = True)
    
    # Get the currently logged-in user.
    current_user = request.user    
    
    reports = Evaluator.objects.filter(creator=visiting_user, report_genarated=True).order_by('-update_date')
    
    page = request.GET.get('page', 1)
    paginator = Paginator(reports, 10)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)
    
  
    context ={
        'visiting_user' : visiting_user,
        'current_user' : current_user,
        'reports' : reports,
          
    }    
    
    # Generate meta data for SEO and page information.
    meta_data = site_info()    
    meta_data['title'] = f'Service of {current_user.username}'
    meta_data['description'] = f"This is the personalized Service page for {current_user.username}. Here, registerd user can view his information and manage services."
    meta_data['tag'] = 'user profile, gf-vp.com'
    meta_data['robots'] = 'noindex, nofollow'
    meta_data['og_image'] = current_user.usertype.icon.url 
    
    # Update the context with the generated meta data.    
    context.update(
        {
            'site_info' : meta_data,            
        }
    )
    
    # Render the template with the provided context.
    return render(request, 'registration/producer_fules.html', context = context)
    
    
    

    
    
    






    
    
    
    
    
    
    

