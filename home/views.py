from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from doc.models import ExSite

from home.models import Quotation
from .forms import UserForm, ProfileForm, PasswordChangeForm, QuestionForm, OptionForm, QuotationForm, NextActivitiesOnQuotation
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from accounts.decorators import expert_required, producer_required, consumer_required, marine_required
from accounts.models import User, UserType
from accounts.helper import check_type
from gfvp import null_session
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect, render, get_object_or_404
from evaluation.models import *
from django.forms import formset_factory, inlineformset_factory
from django.core.exceptions import PermissionDenied
from .helper import users_under_each_label, reports_under_each_biofuel, weeks_results, all_reports, total_reports, typewise_user
from django.db.models import Count, Min
from doc.doc_processor import site_info
from blog.models import BlogPost
from django.templatetags.static import static
import requests
import logging
log =  logging.getLogger('log')





def home(request):
    #skip session error
    null_session(request)  
    # pass user type  
    
    log.info(f'Home page accessed by_____________ {request.user}')
    
    user_types = UserType.objects.all().order_by('sort_order') 
    latest_blogs = BlogPost.published.filter(status = 'published').order_by('-publish')[:3]
    
    #meta
    meta_data = site_info()    
    meta_data['title'] = 'Home'
    # meta_data['meta_name'] = 'Green Fuel Validation Platform'
    meta_data['url'] = request.build_absolute_uri(request.path)
    meta_data['description'] = 'New international platform will help increase supply for sustainable fuels for the marine market!'
    meta_data['tag'] = 'green, fuel, validation, marine, biofuel, alfa, laval, MASH, MAN, ENERGY'
    meta_data['robots'] = 'index, follow'
    meta_data['og_image'] = site_info().get('og_image')
    
    
    context = {
        'user_types': user_types ,        
        'latest_blogs' : latest_blogs,
        'site_info' : meta_data     
    }
    return render(request, 'home/index.html', context = context)


def user_types(request, slug):

    '''
    Types of user are listed here. User signup journey must be started from here by selecting desired user type.
    Same type of user and admin and staff can have permission to visit this page
    '''  
    
    
    #skipp error
    null_session(request)    
    log.info(f'User type page accessed by_____________ {request.user}')
    
    #role player
    request.session['interested_in'] = slug      
    
    
    # ensire user logged to evaluation enrolment 
    try:
        curent_user_type_slug = request.user.usertype.slug
    except:
        curent_user_type_slug = None   
        
    if request.user.is_authenticated:    
        if slug == curent_user_type_slug and request.user.is_producer and (request.user.is_staff and request.user.is_superuser):        
            enroll = {
                'Enroll Evaluation' : reverse('evaluation:evaluation2') 
                }
        elif slug == curent_user_type_slug and request.user.is_marine and (request.user.is_staff and request.user.is_superuser):
            enroll = {
                'Questions' : reverse('home:questions')
                } 
        elif slug == curent_user_type_slug and request.user.is_expert and (request.user.is_staff and request.user.is_superuser):
            enroll = {
                'Quotations' : reverse('home:quotations')
                } 
        elif slug == curent_user_type_slug and request.user.is_producer:
            enroll = {
                'Enroll Evaluation' : reverse('evaluation:evaluation2') 
                }
        elif slug == curent_user_type_slug and request.user.is_marine:
            enroll = {
                'Questions' : reverse('home:questions')
                }       
        elif slug == curent_user_type_slug and request.user.is_expert:
            enroll = {
                'Quotations' : reverse('home:quotations')
                }  
        else:
            enroll = {'Thank You for Joining!' : reverse('accounts:user_link', args=[str(request.user.username)])}
    else:
        enroll = {}
    
    # pass user type data    
    try:
        user_type = UserType.objects.get(slug = slug)
        users = User.objects.filter(usertype = user_type)
    except:
        user_type = None
        users = None
        
        
    #meta
    meta_data = site_info()    
    meta_data['title'] = user_type.name if user_type is not None else 'Page for Biofuel User Type'
    # meta_data['meta_name'] = 'Green Fuel Validation Platform'
    meta_data['url'] = request.build_absolute_uri(request.path)
    meta_data['description'] = f'This is the page for {user_type.name if user_type is not None else "user type registered in our platform"}. This is not a indivisual page for a registered user!!'
    meta_data['tag'] = 'biofuel, usertype, consumer, producer, experts, marine'
    meta_data['robots'] = 'index, follow'
    meta_data['og_image'] = user_type.icon.url
    
    context = {
        'user_type': user_type,
        'users': users,
        'enroll': enroll,
        'site_info' : meta_data         
    }
    return render(request, 'home/usertypes.html', context = context) 
    


@login_required
def dashboard(request):
    #skipping session error essential for signup process
    null_session(request)  
    
    log.info(f'Dashboard accessed by_____________ {request.user}')
    
    #dashboard summary
    
    day_of_week = [key.split(': ') for key, value in weeks_results(request).items()]    
    total_of_day = [value for key, value in weeks_results(request).items()]   
     
    
    #meta
    meta_data = site_info()    
    meta_data['title'] = 'Dashboard'
    # meta_data['meta_name'] = 'Green Fuel Validation Platform'
    meta_data['url'] = request.build_absolute_uri(request.path)
    meta_data['description'] = f'The Dashboard displays the consolidated reports and allows approved user types to perform some limited administrative operations.'
    meta_data['tag'] = 'biofuel, dashboard, operation'
    meta_data['robots'] = 'noindex, nofollow'
    # meta_data['og_image'] = user_type.icon.url
    
    context = {
        'user_of_labels' : users_under_each_label(request),
        'biofuel_records' : reports_under_each_biofuel(request),
        'day_of_week': day_of_week,
        'total_of_day': total_of_day,  
        'total_reports': total_reports(request),      
        'allreports' : all_reports(request),
        'typewise_user' : typewise_user(request),
        'site_info' : meta_data      
    }   
    
    return render(request, 'home/dashboard.html', context = context)

@login_required
def user_setting(request):   
    null_session(request) 
    log.info(f'User setting page accessed by_____________ {request.user}')
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        
        if user_form.is_valid():
            user_form.save()
            messages.success(request,('Your profile was successfully updated!'))		    
        elif profile_form.is_valid():
            profile_form.save()
            messages.success(request,('Your profile data was successfully updated!'))
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, profile_form.errors)
            messages.error(request, user_form.errors)            
        
        return HttpResponseRedirect(reverse('home:user_settings'))
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)  
    
    #meta
    meta_data = site_info()    
    meta_data['title'] = 'User Settings'
    # meta_data['meta_name'] = 'Green Fuel Validation Platform'
    meta_data['url'] = request.build_absolute_uri(request.path)
    meta_data['description'] = f'This page is designated to setup user account and user profile.'
    meta_data['tag'] = 'settings, user profile'
    meta_data['robots'] = 'noindex, nofollow'
    # meta_data['og_image'] = user_type.icon.url  
    
    context = {
        "user":request.user,
        "user_form":user_form,
        "profile_form":profile_form, 
        'site_info' : meta_data          
    }
    return render(request, 'home/settings.html', context = context)

@login_required
def password_change(request):   
    null_session(request) 
    log.info(f'Passowrd changed page accessed by_____________ {request.user}')
    if request.method == "POST":        
        password_form = PasswordChangeForm(user=request.user, data=request.POST)        
        if password_form.is_valid():            
            password_form.save()            
            update_session_auth_hash(request, password_form.user)            
            messages.success(request,('Your password was successfully updated!')) 
        else:
            messages.error(request, 'Invalid form submission.')            
            messages.error(request, password_form.errors)      
        
        return HttpResponseRedirect(reverse('home:change_pass'))    
    password_form = PasswordChangeForm(request.user)  
    
    #meta
    meta_data = site_info()    
    meta_data['title'] = 'Change Password'
    # meta_data['meta_name'] = 'Green Fuel Validation Platform'
    meta_data['url'] = request.build_absolute_uri(request.path)
    meta_data['description'] = f'Password is the key to protect account. Here user can manage self password.'
    meta_data['tag'] = 'user, password, change'
    meta_data['robots'] = 'noindex, nofollow'
    # meta_data['og_image'] = user_type.icon.url
    
    context = {
        "user":request.user,        
        "password_form":password_form,
        'site_info' : meta_data   
    }
    return render(request, 'home/change_pass.html', context = context)


# It is DRY helper to get questions based on user expert type
def get_question_of_label(request):
    # Get where user are expert
    curent_user_expert_in = request.user.experts_in
       
    # get that lebels, here value define which one are using for this question
    # if multilabel value is one then this question should be displayed to the multi type of expert.
    label_to_question = Label.objects.filter(name = curent_user_expert_in, value = str(1))
    
    if request.user.is_staff or request.user.is_superuser or request.user.is_marine:
        # Staff of super user are accesable to all questions
        questions = [q for q in Question.objects.filter(is_active = True)]
    else:   
        # Only user that have label of this question as expert can access this. 
        questions = []
        for q in label_to_question:
            if q.question.is_active:
                questions.append(q.question)
            else:
                continue            
    return questions

def child_modal_data(request, id):
    questions = Question.objects.get(id=id)
    
    context = {
        'qquestion': questions      
    }
    
    return render(request, 'home/child_modal_data.html', context = context)
    

@login_required
@expert_required
def quotations(request):  
    '''get questions related to the current user'''
    
    
    # This is essential where login_required
    null_session(request)
    log.info(f'Quotations page accessed by_____________ {request.user}')
        
    # we need permitted question based on expertise type
    questions = get_question_of_label(request)
    
    # build parent          
    parents = []
    for question in questions:        
        if question.is_door == True:
            parents.append(question)
            
            
    #build results of chaptariged questions       
    results = []    
    for parent in parents:         
        data = {
            parent : [child for child in questions if child.parent_question == parent]
        }
        results.append(data)    
    
    #Paginated response
    page = request.GET.get('page', 1)
    paginator = Paginator(results, 12)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
        
    #meta
    meta_data = site_info()    
    meta_data['title'] = 'Quotations'
    # meta_data['meta_name'] = 'Green Fuel Validation Platform'
    meta_data['url'] = request.build_absolute_uri(request.path)
    meta_data['description'] = f'Every question is allowed to include one or more quotations.  It is created by the biofuel experts.'
    meta_data['tag'] = 'quotation, quotations'
    meta_data['robots'] = 'noindex, nofollow'
    # meta_data['og_image'] = user_type.icon.url
    
    context = {
        'questions': results,
        'site_info' : meta_data   
                
    }
    
    return render(request, 'home/quotations.html', context = context)
    



@login_required
@marine_required
def questions(request):  
    '''get questions related to the current user'''    
    
    # This is essential where login_required
    null_session(request)
    log.info(f'Questions page accessed by_____________ {request.user}')  
    # we need permitted question based on expertise type
    questions = get_question_of_label(request)    
    # build parent         
    parents = []
    for question in questions:        
        if question.is_door == True:
            parents.append(question)            
            
    #build results of chaptariged questions       
    results = []    
    for parent in parents:         
        data = {
            parent : [child for child in questions if child.parent_question == parent]
        }
        results.append(data)    
    
    #Paginated response
    page = request.GET.get('page', 1)
    paginator = Paginator(results, 12)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
        
    #meta
    meta_data = site_info()    
    meta_data['title'] = 'Questions'
    # meta_data['meta_name'] = 'Green Fuel Validation Platform'
    meta_data['url'] = request.build_absolute_uri(request.path)
    meta_data['description'] = f'Here is a collection of specialized questions. The questions and their contents are editable by authorized users.'
    meta_data['tag'] = 'question, chapter'
    meta_data['robots'] = 'noindex, nofollow'
    # meta_data['og_image'] = user_type.icon.url
    
    context = {
        'questions': results,
        'site_info' : meta_data    
    }
    
    return render(request, 'home/questions.html', context = context)


@login_required
@expert_required
def add_quatation(request, slug):
    '''
    quotation can be created by indivisual expert
    one question can have one quotation from same user but can be refer to multi question mult time.
    if no quotation can add other wise can edit
    able to see quotation refered by other user.    
    '''  
    
    log.info(f'Quotation adding by_____________ {request.user}')
    
    # if the page is referering from other page we will delete the next_activities session.. it is neccesary to show saved data in the question if coming from another page.
    # and to ensure to active session when clicking on the go button.
    if request.build_absolute_uri(request.path) == request.META.get('HTTP_REFERER', None):
        pass
    else:
        try:
            del request.session['next_activities'] 
        except:
            pass
    
    
    #protect unuseual activity
    try:
        question = Question.objects.get(is_active = True, slug=slug)
    except:
        messages.warning(request, 'Question not found or inactive!')
        return HttpResponseRedirect(reverse('home:add_quatation', args=[str(slug)]))
    
    #if session have activities by clicking go button then we will get the session activities.
    try:
        session_activities = NextActivities.objects.get(id = int(request.session['next_activities'] if 'next_activities' in request.session else 0)) 
    except:
        session_activities = None
    
    #if question exists ca edit other wise can add
    check_quotation = Quotation.objects.filter(test_for = question, service_provider = request.user)
    
    if check_quotation.exists():  
        #we will change the temporary quatation's session next_activities by session activities    
        cq = (Quotation.objects.filter(test_for = question, service_provider = request.user)).first()           
        cq.next_activities = session_activities           
        if 'next_activities' in request.session:   
            #if next activitiy in the session we will change temporary related question which is coming from the session activities.
            (check_quotation.first()).related_questions.set([q for q in session_activities.related_questions.all()]) 
            #the form is using for the selection of temporary next activity            
            na_form = NextActivitiesOnQuotation(instance=cq)
            #as we set the related questions to the quotation from the session activities then it will select with replacement by overwriting default saved value.
            #please be noted: default new set will remain unchanged until click on the add_quatation as we are deleting session of next activity after saving the quotation.
            form = QuotationForm(instance=check_quotation.first())             
        else:
            #Which we will select it will display
            na_form = NextActivitiesOnQuotation(initial={'test_for': question, 'next_activities':request.session['next_activities'] if 'next_activities' in request.session else cq.next_activities})  
            #will display default behaviour.
            form = QuotationForm(instance=check_quotation.first())      
        
        report_link = reverse('home:quotation_report', kwargs={'question': str(slug), 'quotation': int(check_quotation.first().id) })             
    else:
        if 'next_activities' in request.session:           
            form = QuotationForm(initial={'test_for': question, 'next_activities':session_activities, 'related_questions' :[q for q in session_activities.related_questions.all()]}) 
        else:
            form = QuotationForm(initial={'test_for': question}) 
        #bound to the session
        na_form = NextActivitiesOnQuotation(initial={'test_for': question, 'next_activities':session_activities})   
        report_link = '#'
    
    
    # overwriting form's default queryset for related_questions to restrict access for other domain expert
    questions_id  = [q.id for q in get_question_of_label(request) if not q.is_door ] 
    form.fields["related_questions"].queryset = Question.objects.filter(is_active = True, id__in=questions_id)
    
    
    if request.method == "POST":           
        if 'go' in request.POST: 
            request.session['next_activities'] = request.POST['next_activities']
            return HttpResponseRedirect(reverse('home:add_quatation', args=[str(slug)]))
         
        elif 'add_quatation' in request.POST:
            form = QuotationForm(request.POST,  request.FILES, instance=check_quotation.first(), initial={'test_for': question} )  
            test_for  = request.POST.get('test_for')        
            if question.id == int(test_for):
                if form.is_valid():
                    
                        
                    new_quatation = form.save(commit=False)
                    new_quatation.service_provider = request.user
                    new_quatation.next_activities = (NextActivities.objects.get(id = int(request.session['next_activities']))) if 'next_activities' in request.session else form.cleaned_data['next_activities']
                    require_document = form.cleaned_data['require_documents']
                    related_question = form.cleaned_data['related_questions']
                    new_quatation.save()
                    #essential to set manytomny reltionship
                    new_quatation.require_documents.set(require_document)
                    new_quatation.related_questions.set(related_question) 
                    
                    
                    #after saving data we will delet the session of next activities.
                    try:
                        del request.session['next_activities']
                    except:
                        pass
                    
                    messages.success(request,('Quatation was successfully updated!'))
                    return HttpResponseRedirect(reverse('home:add_quatation', args=[str(slug)]))
                else:
                    messages.error(request, 'Invalid form submission.')
                    messages.error(request, form.errors)      
                    return HttpResponseRedirect(reverse('home:add_quatation', args=[str(slug)]))            
                    
            else:
                messages.warning(request, f'Change in "Tests for question" is not allowed! It should be "{question}"! Changes was not effected.')
                return HttpResponseRedirect(reverse('home:add_quatation', args=[str(slug)]))
    #meta
    meta_data = site_info()    
    meta_data['title'] = 'Add/edit Quotation'
    # meta_data['meta_name'] = 'Green Fuel Validation Platform'
    meta_data['url'] = request.build_absolute_uri(request.path)
    meta_data['description'] = f'The place to add or edit quotation under specific question by the marine expert.'
    meta_data['tag'] = 'quotation'
    meta_data['robots'] = 'noindex, nofollow'
    # meta_data['og_image'] = user_type.icon.url
    
    context = {
        'question': question,
        'form' : form,
        'na_form' : na_form,
        'quatation' : check_quotation.first(), 
        'report_link' : report_link,
        'site_info' : meta_data    
    }
    return render(request, 'home/add_quatation.html', context = context)

#helper function
def get_verbose_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()

# sub function for making PDF
@login_required
def quotation_report2(request, quotation_data):
    null_session(request)
    '''
    genarate pdf based on quotation data
    '''
    log.info(f'Quotation report accessed by_____________ {request.user}')
    import io    
    from reportlab.pdfgen import canvas    
    
    from reportlab.lib.styles import ParagraphStyle    
    from reportlab.lib.units import mm, inch
    from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import letter, A4    
    from reportlab.lib.colors import black, blue, red
    from reportlab.platypus import  Paragraph
    
    site_data = site_info()
    
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."    
    c = canvas.Canvas(buffer)
    c.setPageSize(A4)
    c.setTitle(title = f'Quotation for Question #{quotation_data.test_for.sort_order}--Quotation #{quotation_data.id}')
    c.setAuthor(f'www.gf-vp.com')
    c.setCreator(f'www.gf-vp.com')
    c.getPageNumber()
    c.setFont("Times-Roman", 20)
    
    
    #reference to make pdf
    # https://stackoverflow.com/questions/69537038/django-with-reportlab-pdf
    # https://stackoverflow.com/questions/44970128/django-reportlab-generates-empty-pdf
    # https://stackoverflow.com/questions/37697686/python-reportlab-two-items-in-the-same-row-on-a-paragraph
    # https://www.reportlab.com/docs/reportlab-userguide.pdf
    # https://www.youtube.com/watch?v=1x_ACMFzGYM
    # https://www.reportlab.com/dev/docs/tutorial/
    
    c.beginText()  
    
    
    
    #styeles to be added
    left_style_red_head = ParagraphStyle(name="Times", fontName='Times-Roman', fontSize=16, leading=18, textColor= red, alignment=TA_LEFT)
    left_style_red = ParagraphStyle(name="Times", fontName='Times-Roman', fontSize=14, leading=18, textColor= red, alignment=TA_LEFT)
    left_style_black = ParagraphStyle(name="Times", fontName='Times-Roman', fontSize=16, leading=16, textColor= black, alignment=TA_LEFT)
    left_style_black_50 = ParagraphStyle(name="Times", fontName='Times-Roman', fontSize=16, leading=50, textColor= black, alignment=TA_LEFT)
    center_style_80 = ParagraphStyle(name="Times", fontName='Times-Roman', fontSize=12, leading=80, textColor= blue, alignment=TA_CENTER)
    left_style_blue = ParagraphStyle(name="Times", fontName='Times-Roman', fontSize=14, leading=20, textColor= blue, alignment=TA_LEFT)
    right_style_blue = ParagraphStyle(name="Times", fontName='Times-Roman', fontSize=14, leading=20, textColor= blue, alignment=TA_RIGHT)
    left_style_blue_50 = ParagraphStyle(name="Times", fontName='Times-Roman', fontSize=12, leading=12, textColor= red, alignment=TA_LEFT)
    center_style_line = ParagraphStyle(name="Times", fontName='Times-Roman', fontSize=12, leading=14, textColor= blue, alignment=TA_CENTER) 
    
    
    
    data = [       
    ('left_style_red_head' , f'QUOTATION #{quotation_data.id}'),    
    ('left_style_red' , f'Created for question #{quotation_data.test_for.sort_order}'),
    ('left_style_black' , f'-------------------------------------------------------------------------------------'),    
    ('left_style_blue_50' , f'{ quotation_data.test_for }'),  
    ('left_style_black_50' , f'-------------------------------------------------------------------------------------'),   
    ('left_style_black' , f'-------------------------------------------------------------------------------------'),
    ('left_style_red' , f'<u>Questions which are also tested within this quotation::</u>'),   
     
    ]  
    
    
    
       
    aW = 500 # available width and height
    aH = 800    
   
    
    for style, values in data:        
        p = Paragraph(values, locals()[style])        
        w,h = p.wrap(aW, aH) # find required space    
        aH -= h  # reduce the available height starting from first line  
        if w <= aW and h <= aH:
            p.drawOn(c,50,aH)
            aH = aH #protect to be double line          
        else:
            aH = 800
            c.showPage()            
            # raise ValueError('Not enogugh room')
            w,h = p.wrap(aW, aH) # find required space        
            if w <= aW and h <= aH:
                p.drawOn(c,50,aH)
                aH -= h # reduce the available height   
            continue    
    
    
      
    list_item = []
    for related_question in  quotation_data.related_questions.all():
        list_item.append(related_question)        
        
    # p = Paragraph(list_head, left_style_red)
    for index, item in enumerate(list_item):
        p = Paragraph("__{}. {}".format(index + 1, item))
        w,h = p.wrap(aW, aH)
        aH -= h
        if w <= aW and h <= aH:
            p.drawOn(c,50,aH)
            aH = aH
        else:
            aH = 800
            c.showPage()            
            # raise ValueError('Not enogugh room')
            w,h = p.wrap(aW, aH) # find required space        
            if w <= aW and h <= aH:
                p.drawOn(c,50,aH)
                aH -= h # reduce the available height   
            continue 
        
    
      
        
    data = [
        ('left_style_black_50' , f'-------------------------------------------------------------------------------------'),
        ('left_style_black' , f'-------------------------------------------------------------------------------------'), 
        ('left_style_blue' , f'<u>QUOTATION PROVIDED BY:</u>'),
        ('left_style_blue' , f'___creator: {quotation_data.service_provider.get_full_name()}'),         
        ('left_style_blue' , f'___email: {quotation_data.get_email}'),  
        ('left_style_blue' , f'___phone: {quotation_data.get_phone}'),  
        ('left_style_blue' , f'___orgonization: {quotation_data.get_business_name}'),  
        ('left_style_black_50' , f'-------------------------------------------------------------------------------------'),
    ]
        
        
    
    for style, values in data:        
        p = Paragraph(values, locals()[style])        
        w,h = p.wrap(aW, aH) # find required space    
        aH -= h  # reduce the available height starting from first line  
        if w <= aW and h <= aH:
            p.drawOn(c,50,aH)
            aH = aH #protect to be double line          
        else:
            aH = 800
            c.showPage()            
            # raise ValueError('Not enogugh room')
            w,h = p.wrap(aW, aH) # find required space        
            if w <= aW and h <= aH:
                p.drawOn(c,50,aH)
                aH -= h # reduce the available height   
            continue
    data = [
        ('left_style_black' , f'-------------------------------------------------------------------------------------'),
        ('left_style_red' , f'<u>Quotation details:</u>'),  
        ('left_style_blue', ('___' + get_verbose_name(quotation_data, 'price') + (':___' + str(quotation_data.price) + ' ' + str(quotation_data.price_unit)))),
        ('left_style_blue', ('___' + get_verbose_name(quotation_data, 'needy_time') + (':___' + str(quotation_data.needy_time) + ' ' + str(quotation_data.needy_time_unit)))),
        ('left_style_blue', ('___' + get_verbose_name(quotation_data, 'sample_amount') + (':___' + str(quotation_data.sample_amount) + ' ' + str(quotation_data.sample_amount_unit)))),
        ('left_style_blue', ('___' + get_verbose_name(quotation_data, 'require_documents') + (':___' +  ', '.join([str(q) for q in quotation_data.require_documents.all()])))),
        ('left_style_blue', ('___' + get_verbose_name(quotation_data, 'factory_pickup') + (':___' + str(quotation_data.factory_pickup)))),
        ('left_style_blue', ('___' + get_verbose_name(quotation_data, 'comments') + (':___' + str(quotation_data.comments)))),
        ('left_style_black_50' , f'-------------------------------------------------------------------------------------'),
    ]
    
    
    
    
    
    for style, values in data:        
        p = Paragraph(values, locals()[style])        
        w,h = p.wrap(aW, aH) # find required space    
        aH -= h  # reduce the available height starting from first line  
        if w <= aW and h <= aH:
            p.drawOn(c,50,aH)
            aH = aH #protect to be double line          
        else:
            aH = 800
            c.showPage()            
            # raise ValueError('Not enogugh room')
            w,h = p.wrap(aW, aH) # find required space        
            if w <= aW and h <= aH:
                p.drawOn(c,50,aH)
                aH -= h # reduce the available height   
            continue
    
    attachmenturl = request.build_absolute_uri(static(quotation_data.quotation_format.url))
    atta_res = requests.get(attachmenturl)
    
    
    data = [
        
        ('left_style_black' , f'-------------------------------------------------------------------------------------'),
        ('left_style_black' , f'-------------------------------------------------------------------------------------'),        
        ('left_style_blue' , f'___This report has been genarated using {site_info().get("domain")}'),         
        ('left_style_black_50' , f'-------------------------------------------------------------------------------------'),        
        ('left_style_red_head' , f'PLEASE CONSIDER BELOW PAGES UPLOADED BY THE QUOTATION PROVIDER!' if atta_res.status_code == 200 else ''),
    ]
    for style, values in data:        
        p = Paragraph(values, locals()[style])        
        w,h = p.wrap(aW, aH) # find required space    
        aH -= h  # reduce the available height starting from first line  
        if w <= aW and h <= aH:
            p.drawOn(c,50,aH)
            aH = aH #protect to be double line          
        else:
            aH = 800
            c.showPage()            
            # raise ValueError('Not enogugh room')
            w,h = p.wrap(aW, aH) # find required space        
            if w <= aW and h <= aH:
                p.drawOn(c,50,aH)
                aH -= h # reduce the available height   
            continue
    
    c.save() 
       
    buffer.seek(0)
    
    return buffer

@login_required
def quotation_report(request, question, quotation):    
    from PyPDF2 import PdfFileMerger    
    '''return final report with attachment as pdf'''
    
    null_session(request)
    
    
    quotation_id = quotation    
    quotation_data = Quotation.objects.get(id = quotation_id)   
    
    merger = PdfFileMerger()    

    result2 = quotation_report2(request, quotation_data)  
    result = HttpResponse(content_type='application/pdf')
    merger.append(result2)
    attachmenturl = request.build_absolute_uri(static(quotation_data.quotation_format.url))
    atta_res = requests.get(attachmenturl)
    if atta_res.status_code == 200:
        quotation_file = quotation_data.quotation_format          
        merger.append(quotation_file)    
    merger.write(result)
   
    return result

@login_required
@marine_required
def questions_details(request, slug):
    null_session(request)
    log.info(f'Question detail accessed by_____________ {request.user}')
    #controling front end from session
    if 'extra' not in request.session:
        request.session['extra'] = 0
    
    #validating question is active 
    res_question = get_object_or_404(Question, slug = slug, is_active = True)
    
    #get questions related to the current expert
    curent_user_expert_in = request.user.experts_in    
    if request.user.is_staff or request.user.is_superuser:
        question = res_question
    else:   
        try:
            label_to_question = Label.objects.get(name = curent_user_expert_in, value = str(1), question = res_question)
            question = label_to_question.question
        except:
            raise PermissionDenied   
    
    #option form set of question.
    OptionFormSet = inlineformset_factory(Question, Option, fk_name='question', form = OptionForm, extra= int(request.session['extra']), can_delete=False)    
    if request.method == 'POST':      
        #build combined form
        question_form = QuestionForm(request.POST, request.FILES, prefix='questions', instance=question)        
        option_formset = OptionFormSet(request.POST, request.FILES, prefix='options', instance=question)
        
        
        if question_form.is_valid() and option_formset.is_valid():
            question = question_form.save()
            option_formset = OptionFormSet(request.POST, request.FILES, prefix='options', instance=question)
            option_formset.is_valid()
            option_formset.save() 
            
            #controling fronend with htmx
            request.session['extra'] = 0
            if 'add_more' in request.POST or 'extra' in request.POST:
                return HttpResponseRedirect(reverse('home:questions_details', args=[str(slug)])) 
            else:
                return HttpResponseRedirect(reverse('home:questions'))
            
        else:
            return render(request, 'home/questions_details.html', {
                'question': question,
                'question_form': question_form,
                'option_formset': option_formset,
            })
            
    else:
        question_form = QuestionForm(prefix='questions', instance=question)
        option_formset = OptionFormSet(prefix='options', instance=question)
        
    #meta
    meta_data = site_info()    
    meta_data['title'] = 'Question in edit mode'
    # meta_data['meta_name'] = 'Green Fuel Validation Platform'
    meta_data['url'] = request.build_absolute_uri(request.path)
    meta_data['description'] = f'This is the place to view indivisual question in edit mode.'
    meta_data['tag'] = 'Question'
    meta_data['robots'] = 'noindex, nofollow'
    # meta_data['og_image'] = user_type.icon.url
    
    
    
    context = {
        'question': question,
        'question_form': question_form,
        'option_formset': option_formset,
        'site_info' : meta_data   
        
    }
    return render(request, 'home/questions_details.html', context = context)

@login_required
@marine_required
def new_questions(request):
    null_session(request)
    log.info(f'New question beeing added by_____________ {request.user}')
    if 'extra' not in request.session:
        request.session['extra'] = 0
    OptionFormSet = inlineformset_factory(Question, Option, fk_name='question', form = OptionForm, extra= 3, can_delete=False)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES, prefix='questions')
        
        option_formset = OptionFormSet(request.POST, request.FILES, prefix='options')
        if question_form.is_valid() and option_formset.is_valid():
            question = question_form.save()
            option_formset = OptionFormSet(request.POST, request.FILES, prefix='options', instance=question)
            option_formset.is_valid()
            option_formset.save()
            request.session['extra'] = 0
            if 'add_more' in request.POST or 'extra' in request.POST:
                return HttpResponseRedirect(reverse('home:questions_details', args=[str(question.id)]))
            else:
                return HttpResponseRedirect(reverse('home:questions'))
            
        else:
            return render(request, 'home/new_question.html', {
                
                'question_form': question_form,
                'option_formset': option_formset,
            })
            
    else:
        question_form = QuestionForm(prefix='questions')
        option_formset = OptionFormSet(prefix='options')
        
    #meta
    meta_data = site_info()    
    meta_data['title'] = 'Add New Question'
    # meta_data['meta_name'] = 'Green Fuel Validation Platform'
    meta_data['url'] = request.build_absolute_uri(request.path)
    meta_data['description'] = f'Here new question can be added by the marine expert. The added question will be justified and reformated by the Admin.'
    meta_data['tag'] = 'Question'
    meta_data['robots'] = 'noindex, nofollow'
    # meta_data['og_image'] = user_type.icon.url
    
    
    
    context = {
        
        'question_form': question_form,
        'option_formset': option_formset,
        'site_info' : meta_data    
        
    }
    return render(request, 'home/new_question.html', context = context)

@login_required
@producer_required
def allreports(request):  
    null_session(request)
    
    log.info(f'All report accessed by_____________ {request.user}')
    
    #meta
    meta_data = site_info()    
    meta_data['title'] = 'Evaluation reports of Biofuels.'
    # meta_data['meta_name'] = 'Green Fuel Validation Platform'
    meta_data['url'] = request.build_absolute_uri(request.path)
    meta_data['description'] = f'Report genareted by the biofuel producer are listed here. Admin can see all reports and reports created by the producer can see self reports.'
    meta_data['tag'] = 'biofuel, evaluation, reports'
    meta_data['robots'] = 'noindex, nofollow'
    # meta_data['og_image'] = user_type.icon.url
    
    
    context = {
        'allreports' : all_reports(request), 
        'site_info' : meta_data         
    }
    
    return render(request, 'home/all_reports.html', context = context)


from django.forms import formset_factory
def check_type_to_get_expert(request):
    user_type_id = request.POST.get('usertype')
    user_type = UserType.objects.get(id = user_type_id)
    request.session['interested_in'] = user_type.slug    
    if user_type.is_expert:
        request.session['hidden'] = ''
    else:
        request.session['hidden']  = "hidden"
    
    return HttpResponseRedirect(reverse_lazy('accounts:signup'))

def add_extra(request, pk):   
    request.session['extra'] += 1
    return HttpResponseRedirect(reverse_lazy('home:questions_details', args=[str(pk)]))
def sub_extra(request, pk):    
    if request.session['extra'] >= 1:
        request.session['extra'] -= 1
    return HttpResponseRedirect(reverse_lazy('home:questions_details', args=[str(pk)]))


def webmanifest(request):
    site = site_info() 
    icons = []    
    ic192 = {
        "src": static(site.get('og_image')),
        "sizes": "192x192",
        "type": "image/png"        
    }
    
    icons.append(ic192)   
    ic512 = {
        "src": static(site.get('og_image')),
        "sizes": "512x512",
        "type": "image/png"        
    }
    icons.append(ic512)    
    
    site_data = {
        'name' : site.get('name'),
        'short_name' : site.get('name'),
        'icons' : icons,  
        'start_url' : '/', 
        "scope": "/",
        'lang' : 'en',
        'screenshots' : [static(site.get('og_image')), static(site.get('site_logo'))],     
        'description': site.get('site_description'),  
        "theme_color": "#08793B",
        "background_color": "#08793B",
        "display": "standalone"        
    }
    
    return JsonResponse(site_data, safe=False)




