from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect

from home.models import Quotation
from .forms import UserForm, ProfileForm, PasswordChangeForm, QuestionForm, OptionForm, QuotationForm
from django.contrib import messages
from django.urls import reverse, reverse_lazy
# from django.contrib.auth.forms import PasswordChangeForm
from accounts.decorators import expert_required, producer_required, consumer_required
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


def home(request):
    null_session(request)
    
    user_types = UserType.objects.all().order_by('sort_order') 
    context = {
        'user_types': user_types        
    }
    return render(request, 'home/index.html', context = context)


def user_types(request, slug):
    null_session(request)    
    request.session['interested_in'] = slug   
    
    '''Same type of user and admin and staff can have permission to visit this page'''
    
    # check_type(request, slug)
    try:
        curent_user_type_slug = request.user.type.slug
    except:
        curent_user_type_slug = None
        
    
    if slug == curent_user_type_slug:        
        enroll = reverse('evaluation:evaluation2')
    else:
        enroll = ''
        
    try:
        user_type = UserType.objects.get(slug = slug)
        users = User.objects.filter(type = user_type)
    except:
        user_type = None
        users = None
    
    context = {
        'user_type': user_type,
        'users': users,
        'enroll': enroll    
    }
    return render(request, 'home/usertypes.html', context = context) 
    


@login_required
def dashboard(request):
    null_session(request)    
    day_of_week = [key.split(': ') for key, value in weeks_results(request).items()]
    total_of_day = [value for key, value in weeks_results(request).items()]
    
    # print(typewise_user(request))
    
    
    
    context = {
        'user_of_labels' : users_under_each_label(request),
        'biofuel_records' : reports_under_each_biofuel(request),
        'day_of_week': day_of_week,
        'total_of_day': total_of_day,  
        'total_reports': total_reports(request),      
        'allreports' : all_reports(request),
        'typewise_user' : typewise_user(request)
        
    }
    
    
    
    return render(request, 'home/dashboard.html', context = context)

@login_required
def user_setting(request):   
    null_session(request) 
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
    
    context = {
        "user":request.user,
        "user_form":user_form,
        "profile_form":profile_form,
        
    }
    return render(request, 'home/settings.html', context = context)

@login_required
def password_change(request):   
    null_session(request) 
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
    
    context = {
        "user":request.user,        
        "password_form":password_form
    }
    return render(request, 'home/change_pass.html', context = context)



def get_question_of_label(request):
    # Get where user are expert
    curent_user_expert_in = request.user.experts_in
       
    # get that lebels, here value define which one are using for this question
    # if multilabel value is one then this question should be displayed to the multi type of expert.
    label_to_question = Label.objects.filter(name = curent_user_expert_in, value = str(1))
    
    if request.user.is_staff or request.user.is_superuser:
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
    



@login_required
@expert_required
def questions(request):  
    '''get questions related to the current user'''
    
    
    # This is essential where login_required
    null_session(request)
        
    
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
    
    context = {
        'questions': results        
    }
    
    return render(request, 'home/questions.html', context = context)


@login_required
@expert_required
def add_quatation(request, slug):
    
    
    try:
        question = Question.objects.get(is_active = True, slug=slug)
    except:
        messages.warning(request, 'Question not found or inactive!')
        return HttpResponseRedirect(reverse('home:add_quatation', args=[str(slug)]))
    
    check_quotation = Quotation.objects.filter(test_for = question, service_provider = request.user)
    if check_quotation.exists(): 
        form = QuotationForm(instance=check_quotation.first())   
        report_link = reverse('home:quotation_report', kwargs={'question': str(slug), 'quotation': int(check_quotation.first().id) })             
    else:
        form = QuotationForm(initial={'test_for': question}) 
        report_link = '#'
    
    
    # overwriting form's default queryset for related_questions to restrict access for other other domain expert
    questions_id  = [q.id for q in get_question_of_label(request) if not q.is_door ] 
    form.fields["related_questions"].queryset = Question.objects.filter(is_active = True, id__in=questions_id)
    
    
    if request.method == "POST":
        form = QuotationForm(request.POST,  request.FILES, instance=check_quotation.first(), initial={'test_for': question} )  
        test_for  = request.POST.get('test_for')        
        if question.id == int(test_for):
            if form.is_valid():
                new_quatation = form.save(commit=False)
                new_quatation.service_provider = request.user
                related_question = form.cleaned_data['related_questions']
                new_quatation.save()
                new_quatation.related_questions.set(related_question)
                
                messages.success(request,('Quatation was successfully updated!'))
                return HttpResponseRedirect(reverse('home:add_quatation', args=[str(slug)]))
            else:
                messages.error(request, 'Invalid form submission.')
                messages.error(request, form.errors)      
                return HttpResponseRedirect(reverse('home:add_quatation', args=[str(slug)]))            
                
        else:
            messages.warning(request, f'Change in "Tests for question" is not allowed! It should be "{question}"! Changes was not effected.')
            return HttpResponseRedirect(reverse('home:add_quatation', args=[str(slug)]))
        
        
        
    
    
    context = {
        'question': question,
        'form' : form,
        'quatation' : check_quotation.first(),
        'report_link' : report_link
        
        
        
    }
    return render(request, 'home/add_quatation.html', context = context)

def get_verbose_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()

@login_required
def quotation_report2(request, quotation_data):
    null_session(request)
    import io
    from django.http import FileResponse
    from reportlab.pdfgen import canvas    
    from django.template.loader import render_to_string
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle    
    from reportlab.lib.units import mm, inch
    from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.lib.pagesizes import letter, A4    
    from reportlab.lib.colors import Color, black, blue, red
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer    
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
    
    

    # https://stackoverflow.com/questions/69537038/django-with-reportlab-pdf
    # https://stackoverflow.com/questions/44970128/django-reportlab-generates-empty-pdf
    # https://stackoverflow.com/questions/37697686/python-reportlab-two-items-in-the-same-row-on-a-paragraph
    # https://www.reportlab.com/docs/reportlab-userguide.pdf
    # https://www.youtube.com/watch?v=1x_ACMFzGYM
    # https://www.reportlab.com/dev/docs/tutorial/
    
    c.beginText()
    
    
    
    
    
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
        ('left_style_blue' , f'___email: {quotation_data.service_provider.email}'),  
        ('left_style_blue' , f'___phone: {quotation_data.service_provider.phone}'),  
        ('left_style_blue' , f'___orgonization: {quotation_data.service_provider.orgonization}'),  
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
        ('left_style_blue', ('___' + get_verbose_name(quotation_data, 'require_documents') + (':___' + str(quotation_data.require_documents)))),
        ('left_style_blue', ('___' + get_verbose_name(quotation_data, 'factory_pickup') + (':___' + str(quotation_data.factory_pickup)))),
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
        ('left_style_blue' , f'___This report has been genarated using {site_info().get("domain")}'),         
        ('left_style_black_50' , f'-------------------------------------------------------------------------------------'),        
        ('left_style_red_head' , f'PLEASE CONSIDER BELOW PAGES UPLOADED BY THE QUOTATION PROVIDER!'),
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
    null_session(request)
    from PyPDF2 import PdfFileMerger
    
    quotation_id = quotation    
    quotation_data = Quotation.objects.get(id = quotation_id)    
    
    merger = PdfFileMerger()    

    quotation_file = quotation_data.quotation_format
    result2 = quotation_report2(request, quotation_data)  
    result = HttpResponse(content_type='application/pdf')
    merger.append(result2)
    merger.append(quotation_file)    
    merger.write(result)
   
    return result

@login_required
@expert_required
def questions_details(request, slug):
    null_session(request)
    if 'extra' not in request.session:
        request.session['extra'] = 0
    
    res_question = get_object_or_404(Question, slug = slug, is_active = True)
    
    '''get questions related to the current user'''
    curent_user_expert_in = request.user.experts_in
    
    if request.user.is_staff or request.user.is_superuser:
        question = res_question
    else: 
    
        try:
            label_to_question = Label.objects.get(name = curent_user_expert_in, value = str(1), question = res_question)
            question = label_to_question.question
        except:
            raise PermissionDenied   
    
    
    OptionFormSet = inlineformset_factory(Question, Option, fk_name='question', form = OptionForm, extra= int(request.session['extra']), can_delete=False)
    
    if request.method == 'POST':
        
        
        question_form = QuestionForm(request.POST, request.FILES, prefix='questions', instance=question)
        
        option_formset = OptionFormSet(request.POST, request.FILES, prefix='options', instance=question)
        if question_form.is_valid() and option_formset.is_valid():
            question = question_form.save()
            option_formset = OptionFormSet(request.POST, request.FILES, prefix='options', instance=question)
            option_formset.is_valid()
            option_formset.save()
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
    
    
    
    context = {
        'question': question,
        'question_form': question_form,
        'option_formset': option_formset,
        
    }
    return render(request, 'home/questions_details.html', context = context)

@login_required
@expert_required
def new_questions(request):
    null_session(request)
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
    
    
    
    context = {
        
        'question_form': question_form,
        'option_formset': option_formset,
        
    }
    return render(request, 'home/new_question.html', context = context)

@login_required
def allreports(request):  
    null_session(request)
    
    
    context = {
        'allreports' : all_reports(request),
        
    }
    
    return render(request, 'home/all_reports.html', context = context)


from django.forms import formset_factory
def check_type_to_get_expert(request):
    user_type_id = request.POST.get('type')
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




