from pprint import pprint
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from doc.models import ExSite
from home.models import WeightUnit
from .forms import *
from .models import *
from accounts.models import User, UserType
from django.contrib import messages
from django.urls import reverse
from django_xhtml2pdf.utils import generate_pdf
from . helper import label_assesment_for_donot_know, label_assesment_for_positive, overall_assesment_for_donot_know, overall_assesment_for_positive, get_current_evaluator
from django.contrib.auth.decorators import login_required
from accounts.decorators import producer_required
from gfvp import null_session
from django.core.exceptions import PermissionDenied
from youtubesearchpython import VideosSearch
from youtubesearchpython import *

#helper function should be called into the @login_required and @producer_required
def set_evaluation(question, selected_option, evaluator):
    #delete prevous record if have to ensure reentry.
    try:   
        Evaluation.objects.filter(evaluator = evaluator, question = question).delete()    
    except:
        pass
    new_evaluation = Evaluation(evaluator = evaluator, option = selected_option, question = question ) 
    new_evaluation.save()
        
    
#helper function should be called into the @login_required and @producer_required
def set_eva_comments(question, comment, evaluator):    
    #check editing or fresh entry
    evacomments = EvaComments.objects.filter(evaluator = evaluator, question = question)
    if evacomments.exists():
        evacomments = EvaComments.objects.get(evaluator = evaluator, question = question)
        #Ensure new comments
        if comment != '':
            evacomments.comments = comment
            evacomments.save()        
    else:
        new_eva_comment = EvaComments(evaluator = evaluator, question = question, comments = comment)
        new_eva_comment.save()
        
#helper function should be called into the @login_required and @producer_required    
def set_evastatment(request, selected_option, evaluator):    
    question = selected_option.question    
    #delete previous record of this option
    try:
        EvaLebelStatement.objects.filter(question = question, evaluator = evaluator, assesment = False).delete()   
    except:
        pass 
    
    set_labels = Label.objects.filter(question =  question, value = 1)
    for set_label in set_labels:
        defined_label = DifinedLabel.objects.get(name = set_label.name)
        eva_label = EvaLabel.objects.get(label = defined_label, evaluator = evaluator)
        new_evalebel_statement = EvaLebelStatement(evalebel = eva_label, option_id = selected_option.id, statement = selected_option.statement, next_step = selected_option.next_step, dont_know = selected_option.dont_know, question = selected_option.question, positive = selected_option.positive, evaluator =  evaluator)
        new_evalebel_statement.save()
        try:
            EvaLebelStatement.objects.filter(evalebel = eva_label, evaluator = evaluator, assesment = True).delete()
        except:
            # pass is essential to execute rest of the code
            pass
        
        #This is a calculated assesment based on the answere. Called function gives the idea.    
        summery_statement_do_not_know = EvaLebelStatement(evalebel = eva_label, statement = label_assesment_for_donot_know(request, eva_label, evaluator),  evaluator =  evaluator, assesment = True)
        summery_statement_do_not_know.save()

        #This is a calculated assesment based on the answere. Called function gives the idea.    
        summery_statement_positive = EvaLebelStatement(evalebel = eva_label, statement = label_assesment_for_positive(request, eva_label, evaluator),  evaluator = evaluator, assesment = True)
        summery_statement_positive.save()
        
        
        
#helper function should be called into the @login_required and @producer_required       
def set_evastatement_of_logical_string(request, selected_option, evaluator):    
    #review and revise the logical string
    '''
    Making option set based on logical string
    As it is based on multi logicalSting so It can be more hactic to call from signal. or it can be called from cronjob.
    Cronjob can be implemented later to reduce the process load during adding option to the report.
    So Each time of option submitting, we will check if anychange in logicalStrngs and will edit optionset acordingly.
    Then wil be comitted to the report.     
    '''
    logical_strings = LogicalString.objects.all()
    
    logical_options = []
    for logical_string in logical_strings:
        ls_id = logical_string.id
        text = logical_string.text
        overall = logical_string.overall
        positive = logical_string.positive
        sting_options = logical_string.options.all()
        option_list = []
        for s_o in sting_options:
            option_list.append(str(s_o.id))
        logical_options.append(option_list)

        try:
            '''
            edit if any changed
            '''
            option_set = OptionSet.objects.get(option_list = option_list)
            option_set.id = ls_id
            option_set.text = text
            option_set.overall = overall
            option_set.positive = positive
            option_set.save()
        except Exception as e:
            '''
            delete changed to re input
            '''
            lo_except_last = [x for x in logical_options if x != option_list]
            unmatched = [item for item in logical_options if not item in lo_except_last ]
            try:
                for u in unmatched:
                    OptionSet.objects.get(option_list = u).delete()
            except Exception as e:
                pass
            new_option_set = OptionSet(option_list = option_list, text = text, overall = overall , positive = positive, ls_id = ls_id )
            new_option_set.save()
            
    
    defined_common_label = DifinedLabel.objects.get(common_status = True)    
    eva_label_common = EvaLabel.objects.get(label = defined_common_label, evaluator = evaluator)
    eva_statement = EvaLebelStatement.objects.filter(evaluator = evaluator)   
    
    
    #delete any prevous record for this current report
    try:
        EvaLebelStatement.objects.filter(evalebel = eva_label_common, evaluator =  evaluator, assesment = True).delete()    
    except:
        pass
    
    
    #This is a calculated assesment based on the answere. Called function gives the idea.    
    summery_statement_do_not_know = EvaLebelStatement(evalebel = eva_label_common, statement = overall_assesment_for_donot_know(request, eva_label_common, evaluator),  evaluator =  evaluator, assesment = True)
    summery_statement_do_not_know.save()
    #This is a calculated assesment based on the answere. Called function gives the idea.    
    summery_statement_positive = EvaLebelStatement(evalebel = eva_label_common, statement = overall_assesment_for_positive(request, eva_label_common, evaluator),  evaluator =  evaluator, assesment = True)
    summery_statement_positive.save()
    
    

    try:
        '''
        Make as it is optionset have saved in database.
        '''
        es_option_id = set()
        for es in eva_statement:
            es_option_id.add(es.option_id)
        eoi = list(es_option_id)
        
        
        # Check and set to the summary.
        logical_statement = OptionSet.objects.get(option_list = eoi)
        if (eoi in logical_options) and (logical_statement.overall == str(1)):
            try:
                EvaLebelStatement(evalebel = eva_label_common, evaluator =  evaluator, positive = logical_statement.positive,).delete()
            except:
                pass
            new_evalebel_statement_common = EvaLebelStatement(evalebel = eva_label_common, statement = logical_statement.text, evaluator =  evaluator, positive = logical_statement.positive,)
            new_evalebel_statement_common.save()
            
        # Check and set to the specific label.    
        if (eoi in logical_options) and (logical_statement.overall == str(0)):
            ls_labels = Lslabel.objects.filter(logical_string =  logical_statement, value = 1)
            for ls_label in ls_labels:
                defined_label = DifinedLabel.objects.get(name = ls_label.name)
                ls_eva_label = EvaLabel.objects.get(label = defined_label, evaluator = evaluator)
                try:
                    EvaLebelStatement(evalebel = ls_eva_label, evaluator =  evaluator, positive = logical_statement.positive,).delete()
                except:
                    pass
                new_evalebel_statement_g = EvaLebelStatement(evalebel = ls_eva_label, statement = logical_statement.text, evaluator =  evaluator, positive = logical_statement.positive,)
                new_evalebel_statement_g.save()      
                  
    except Exception as e:        
        pass
    
    #Statement of the option will be aded to the summary if overall is set to 1    
    if selected_option.overall == str(1):
        try:
            EvaLebelStatement(evalebel = eva_label_common, evaluator =  evaluator, assesment = False).delete()
        except:
            pass
        new_evalebel_statement_common = EvaLebelStatement(evalebel = eva_label_common, option_id = selected_option.id, statement = selected_option.statement, evaluator =  evaluator)
        new_evalebel_statement_common.save()    
    
        
        

def option_add2(request):    
    #Ensure session started
    #as report session can not be started without authenticated user
    try:
        Evaluator.objects.get(id = request.session['evaluator'])
    except:
        messages.warning(request, "What you're trying to do isn't a good idea!")
        return HttpResponseRedirect(reverse('evaluation:evaluation2'))   
    
    #essential part for authenticated user where logedin_required
    null_session(request) 
    
    if request.method == 'POST':        
        
        question_slug = request.POST['slug']       
        option_id = request.POST['option_id'] 
        comment = request.POST['comment']
        
        
        #checking options from server side, if frontend skipped by anyhow.        
        if 'option_id' not in request.POST:
            messages.warning(request, 'To proceed, please select an option!')
            return HttpResponseRedirect(reverse('evaluation:eva_question', args=[int(request.session['evaluator']), str(question_slug)]))       
        
        
        question = Question.objects.get(slug = question_slug)        
        selected_option = Option.objects.get(id = option_id) 
        
        
        # to check feedback of the option and to submit the comments.
        # I was not agree to this part as it consume more resource and which is unnecessary as 
        # I showed the result by tooltips on the frontend
        # But it was requirment.
        if 'get_feedback' in request.POST:
            # save or update by checking existing coments of user of this report is exist.
            set_eva_comments(question, comment,  get_current_evaluator(request) )
            #save or update evaluation by checking existing evaluation
            set_evaluation(question, selected_option, get_current_evaluator(request))  
            return HttpResponseRedirect(reverse('evaluation:eva_question', args=[int(request.session['evaluator']), str(question_slug)]))
        
        #check Option Submitted or not
        #This is for first time.
        try: 
            Evaluation.objects.get(evaluator = get_current_evaluator(request), question = question).option
        except:
            messages.warning(request, 'To proceed, please select an option!')
            return HttpResponseRedirect(reverse('evaluation:eva_question', args=[int(request.session['evaluator']), str(question_slug)]))          
        
        
        #re-confirm to avoid oparation mistak. as an unnecessary function running from client recomendation
        set_evaluation(question, selected_option, get_current_evaluator(request))  
        
        #control adding or editing
        set_evastatment(request, selected_option, get_current_evaluator(request))     
           
        #control adding or editing
        set_evastatement_of_logical_string(request, selected_option, get_current_evaluator(request))
        
        
        #try to find next question if not found report will be genarated and the report(Evaluator) will mark as genarated.
        try:  
            # to forward to next question after submitting a question.          
            next_question = selected_option.next_question  
            
            #This will force user to go to the question if trying to access initial page of evaluation.      
            request.session['question'] = next_question.slug            
        except:            
            #Mark report as genarated. if no next question found and redirect to Thanks page.                  
            evaluator = Evaluator.objects.get(id = request.session['evaluator'])            
            evaluator.report_genarated = True
            evaluator.save()
            return HttpResponseRedirect(reverse('evaluation:thanks'))
        
        #It is for manual submission but button hide in front-end
        if 'submit_and_stay' in request.POST:   
            return HttpResponseRedirect(reverse('evaluation:eva_question', args=[int(request.session['evaluator']), question_slug]))
        
        #It is for automatic detection where to go to next based on selection of admin
        if 'submit_and_auto' in request.POST:            
            return HttpResponseRedirect(reverse('evaluation:eva_question', args=[int(request.session['evaluator']), next_question.slug]))
        

#To check question button and mark with specific color by template
def question_dataset(request):
    '''
    get sorted question of current report.
    mark all question have in this report.
    get last question have in this report
    check any unmark before this question
    check anything after this question.
    check if do not know
    check if 'no'    
    '''
    #sort_order is most important here
    # childs = Question.objects.filter(is_door =False, is_active = True).order_by('sort_order')
    stored_questions = Question.objects.filter(is_active = True).order_by('sort_order')   
    
    #build parentwise shorted question    
    questions = []
    for question in stored_questions:
        if question.is_door == True:
            questions.append(question)            
            questions.extend([child for child in stored_questions if child.parent_question == question])   
    
    #Pul answered record of the current report
    evaluations = Evaluation.objects.filter(evaluator = get_current_evaluator(request)).order_by('id')
    questions_of_report = []
    for evaluation in evaluations:
        questions_of_report.append(evaluation.question)  
    
    
    #set temporary status of questions    
    for question in questions:
        if question in questions_of_report:
            setattr(question, 'stat', 'checked') 
        else:
            setattr(question, 'stat', 'skipped')           
    
    #modify status after checked
    try:
        stop_index = max([i for i, j in enumerate([question.stat for question in questions]) if j == 'checked'])       
        for question in questions[int(stop_index) + 1:]:          
            if question.stat == 'skipped':            
                setattr(question, 'stat', 'unchecked')
            else:            
                continue
    except:
        for question in questions:          
            if question.stat == 'skipped':            
                setattr(question, 'stat', 'unchecked')
            else:            
                continue
        
    #if dont know or no    
    for question in questions:
        try:
            get_option = Evaluation.objects.get(evaluator = get_current_evaluator(request), question = question).option
            if get_option.dont_know == True or  get_option.name == 'No':
                setattr(question, 'stat', 'skipped')
            else:
                continue                
        except:
            pass
        
    # if parent is skipped
    for question in questions:
        if question.is_door == True and question.stat == 'skipped':
            childs = [child for child in questions if child.parent_question == question]            
            for child in childs:
                setattr(child, 'stat', 'skipped')
                Evaluation.objects.filter(question = child, evaluator = get_current_evaluator(request)).delete()  
                
        
    parents = []
    for question in questions:        
        if question.is_door == True:
            parents.append(question)
            
    #build results of chaptariged questions       
    results = {}    
    for parent in parents:         
        data = {
            parent : [child for child in questions if child.parent_question == parent]
        }
        results.update(data)       
            
    
    return results

    
'''
====
Main interface during evaluation process.
====
'''
@login_required
@producer_required
def eva_question(request, evaluator, slug):
    
    #This is essential where user loggedin
    null_session(request)    
    
    '''
    ========
    Part of report Editing
    ========
    Ensure that report genarator coming from initial page.
    Without initial data no report can be build.    
    if any incomplete report in this browser no report can be edited. 
    To complte the report user should click to the "get last report" button from the thank you page.
    Yes Question should be marked as True under Yes status
    No Type Question should have name 'No'(case sensative)
    Don't Know Question Should be marked as True in Don't Know Status Column.
    '''
       
    if 'evaluator' not in request.session:
        messages.warning(request, 'You are not permitted to access the requested webpage!')
        return HttpResponseRedirect(reverse('evaluation:evaluation2'))    
    
    '''
    if anybody coming from initial page then system will get session evaluator
    if no report is in progress evaluator will be '' . it is ensured by middleware.
    if anybody going to edit report then report id will be taken as session evaluator.
    '''
    if request.session['evaluator'] == '':
        request.session['evaluator'] = evaluator
        edit_evaluator = Evaluator.objects.get(id = evaluator)        
        edit_evaluator.report_genarated = False
        edit_evaluator.save()      
    
    '''
    Below evaluator checking will ensure the correct report are editing.
    Otherwise user will put data by thinking one report but data can be edited in another report. Things can be messy.
     
    ''' 
    if request.session['evaluator'] !=  evaluator:            
        messages.warning(request, f"You have an active, unfinished Report, Report#{request.session['evaluator']}! So you're not permitted to perform this procedure!")        
        return HttpResponseRedirect(reverse('accounts:user_link', args=[str(request.user.username)]))     
    
    question = Question.objects.get(slug = slug)   
    
    '''
    =====
    Parent's ans Must be 'Yes' before giving ans to any child
    =====
    if is_door will not check anything.
    if not door system will checked all answered question of this report that have this question or not.
    if question have will check is it 'Yes' or not.
    if 'Yes' User will be able to ans to the child of this parent
    otherwise will give message and will not allow to go to inside.    
    '''
    if question.is_door:
        pass
    else:
        parent = question.parent_question
        evaluations = Evaluation.objects.filter(evaluator = get_current_evaluator(request)).order_by('id')
        questions_of_report = []
        for evaluation in evaluations:
            questions_of_report.append(evaluation.question) 
        try:
            get_option = Evaluation.objects.get(evaluator = get_current_evaluator(request), question = parent).option
            if parent not in questions_of_report or get_option.yes_status == False:
                messages.warning(request, 'To go inside this block, you must answer "Yes" to the specified question!')
                return HttpResponseRedirect(reverse('evaluation:eva_question' ,  args=[int(evaluator),  str(parent.slug)]))  
        except:            
            messages.warning(request, 'To go inside this block, you must answer "Yes" to the specified question!')
            return HttpResponseRedirect(reverse('evaluation:eva_question' ,  args=[int(evaluator), str(parent.slug)]))  
        
    
    '''
    The qualified rang can be set from Admin>>Site>>qualified ans rang
    '''
    qualified_ans_rang = int(ExSite.on_site.get().qualified_ans_range)
    
        
    options = Option.objects.filter(question = question)
    evaluator_data = get_current_evaluator(request)
    eva_lebels = EvaLabel.objects.filter(evaluator = evaluator_data).order_by('sort_order')
    
    
    request.session['total_question'] = Evaluation.objects.filter(evaluator = evaluator).count()  
    total_ques = Question.objects.all().count() - request.session['total_question']
    timing_text = f"Depending on how many answers you provide, the self assessment will take anywhere from {round(total_ques/10)} to {round(total_ques/3)} minutes. At the end of the assessment, a PDF report will be provided, which can be retrieved via the Dashboard at a later stage."
    
    
    try:
        submitted_comment = EvaComments.objects.get(evaluator = get_current_evaluator(request), question = question).comments
    except:
        submitted_comment = None   
    
      
    try:
        selected_option = Evaluation.objects.get(evaluator = get_current_evaluator(request), question = question).option
    except:
        selected_option = None  
        
        
    chart_data = StandaredChart.objects.filter(question = question)  
    
    
    search_term = str(question.name) + ', ' +  str(get_current_evaluator(request).biofuel.name)
    
    videosSearch = VideosSearch(search_term, limit = 3)
    vedio_search_result = videosSearch.result()
    
    vedio_urls = []
    for r in vedio_search_result['result']:        
        embed_url = 'https://www.youtube.com/embed/{}'.format(r['id'])
        vedio_urls.append(embed_url)

    
        
    context ={
        'slug' : slug,
        'question_dataset' : question_dataset(request) ,
        'question': question,
        'optns': options,
        'evaluator_data': evaluator_data,
        'eva_lebels': eva_lebels,
        'timing_text': timing_text,    
        'total_question': request.session['total_question'], 
        'qualified_rang' : qualified_ans_rang,   
        'evaluator':evaluator, 
        'selected_option' : selected_option,
        'submitted_comment' : submitted_comment,
        'chart_data' : chart_data,
        'vedio_urls' : vedio_urls,
        'search_term' : search_term
        
    }
    return render(request, 'evaluation/eva_question.html', context = context)

'''
====
Initial Interface for evaluation
====
'''

@login_required
@producer_required
def eva_index2(request):
    '''
    Initial data collection for each evaluation report.
    if were sumitted a question user will be redirected that question
    otherwise will take initial data
    settingup door question is essential by admin 
    '''
    
    #essential part where login_required
    null_session(request)
    
    
    #Preparing guard to check whether system should take initial data or need to forwared to next_question of selected question previously.
    try:
        session_evaluator = Evaluator.objects.get(id = request.session['evaluator'])
    except Exception as e:        
        session_evaluator = False  
        
        
    #get first question of evaluation process based on short_order. If no first question set by admin will redirect to homepage with warning message.
    try:
        first_of_parent = Question.objects.filter(is_door = True).order_by('sort_order').first()        
    except:
        messages.warning(request,'There is something wrong in procedure setting by site admin, Please try again latter!')
        return HttpResponseRedirect(reverse('evaluation:evaluation2'))   
    
    #Scaning by guard
    if (session_evaluator is False) or ('question' not in request.session):
        if request.method == "POST": 
            form = EvaluatorForm(request.POST)
            if form.is_valid():            
                ##take data 
                name = form.cleaned_data['name']
                email = form.cleaned_data['email'] 
                phone = form.cleaned_data['phone']
                orgonization = form.cleaned_data['orgonization']
                biofuel = form.cleaned_data['biofuel']
                
                #genarate report's initial data. It is a basement of a report or evaluation.
                new_evaluator = Evaluator(creator = request.user, name = name, email = email, phone = phone, orgonization = orgonization, biofuel = biofuel )
                new_evaluator.save()
                
                #Catch user record from the evaluation form in not exists
                user = User.objects.get(id = request.user.id)
                first_name = name.split()[0]
                last_name = name.split()[-1]                
                if not user.first_name:
                    user.first_name = first_name
                if not user.last_name != '':
                    user.last_name = last_name
                if not user.orgonization:
                    user.orgonization = orgonization
                if not user.phone:
                    user.phone = phone
                user.save()
                
                #it is count as report id
                request.session['evaluator'] = new_evaluator.id               
                            
                #decide labels.
                defined_label = DifinedLabel.objects.all()
                for dl in defined_label:
                    new_evalabel = EvaLabel(label = dl, evaluator = get_current_evaluator(request), sort_order=dl.sort_order)
                    new_evalabel.save()            
                return HttpResponseRedirect(reverse('evaluation:eva_question' ,  args=[int(request.session['evaluator']), str(first_of_parent.slug)]))
            
        
        else: 
            
            '''
            standalone initial page of evaluation.
            '''           
            try:
                first_reports = Evaluator.objects.filter(creator = request.user, report_genarated = True).order_by('create_date').first()  
                first_biofuel = first_reports.biofuel
                first_report_name = first_reports.name
            except:
                first_reports = None
                first_biofuel = ''
                first_report_name = ''
            
            #rechecking user is authorized or not, although it is not necessary as only logedin user can enter to this page, but it is safe to avoid error if anyhow decorator are removed. There is no resource load.
            if request.user.is_authenticated:
                type = UserType.objects.get(slug = request.user.type.slug )
                name = request.user.get_full_name if request.user.get_full_name else first_report_name
                email = request.user.email
                phone = request.user.phone
                orgonization = request.user.orgonization
            else:
                type = UserType.objects.get(slug = request.session['interested_in'] )
                name = ''
                email = ''
                phone = ''
                orgonization = ''
                
                
            initial_dict = {
            "type" : type,
            "email" : email,
            "phone":phone,
            "orgonization":orgonization,
            "name":name,
            'biofuel' : first_biofuel
            }
            form = EvaluatorForm(initial = initial_dict)
    else:
        '''
        if an active incomplete report user will forwared to the recorde next question.
        Otherwise will go to the first question of evaluation decided by admin.        
        '''
        
        if 'question' in request.session:
            return HttpResponseRedirect(reverse('evaluation:eva_question', args=[int(request.session['evaluator']), str(request.session['question'])]))
        else:
            return HttpResponseRedirect(reverse('evaluation:eva_question' ,  args=[int(request.session['evaluator']), str(first_of_parent.slug)]))
            
    total_ques = Question.objects.all().count()
    box_timing = f"Depending on how many answers you provide, the self assessment will take anywhere from {round(total_ques/10)} to {round(total_ques/3)} minutes. At the end of the assessment, a PDF report will be provided, which can be retrieved via the Dashboard at a later stage."
   
    context ={
        'form': form,
        'box_timing': box_timing,        
    }
    return render(request, 'evaluation/new_index.html', context = context)
    
   
@login_required
@producer_required    
def thanks(request):    
    
    
    #essential part where login_required
    null_session(request)  
    '''
    Deletion of incomplete report are not necessary , if need can uncomments below code. need to check if raising any error.As an incomplete report may not have evalauation or statment both.
    '''  
   
    
    try:
        last_reports = Evaluator.objects.filter(creator = request.user, report_genarated = True).order_by('-create_date').first()  
    except:
        last_reports = None    
    
    #Session evaluator is most important to view calculated result in the thankyou page.
    #By default session's null evaluator has been created by middlewear
    if request.session['evaluator'] == '':        
        return HttpResponseRedirect(reverse('accounts:user_link', args=[str(request.user.username)]))
    
    #Calculation to display on the thankyou page.
    ans_ques = EvaLebelStatement.objects.filter(evaluator = get_current_evaluator(request), question__isnull = False, assesment = False).values('question').distinct().count()
    dont_know_ans = EvaLebelStatement.objects.filter(evaluator = get_current_evaluator(request), question__isnull = False, dont_know = 1, assesment = False).values('question').distinct().count()
    pos_ans = EvaLebelStatement.objects.filter(evaluator = get_current_evaluator(request), question__isnull = False, positive = 1, assesment = False).values('question').distinct().count()
    positive_percent = (int(pos_ans) * 100)/int(ans_ques)
    dont_know_percent = (int(dont_know_ans) * 100)/int(ans_ques)
    
    gretings = 'Thank you very much! Your information has been saved!'
    button = reverse('evaluation:report', args=[last_reports.slug])
    
    '''
    Build all report editing url
    Parent should be selected by admin otherwise site can arise error. 
    '''
    #increadable setattr to reduce time to make report editing url without touch of database
    first_of_parent = Question.objects.filter(is_door = True).order_by('sort_order').first()  
    reports = Evaluator.objects.filter(creator = request.user).order_by('-id')  
    for report in reports:            
        try:   
            last_question = Evaluation.objects.filter(evaluator = report).order_by('id').last().question        
            setattr(report, 'last_slug', last_question.slug )
        except:
            setattr(report, 'last_slug', first_of_parent.slug )
    
       
    
    context = {
        'gretings': gretings,
        'button': button,
        'ans_ques': ans_ques,
        'dont_know_ans': dont_know_ans,
        'pos_ans': pos_ans,
        'positive_percent': str("%.2f" % positive_percent) + '%',
        'dont_know_percent': str("%.2f" % dont_know_percent) + '%',
        'reports': reports,
        'last_reports' : last_reports,
        'complete_report_button_text': 'Confirm and Generate',
        'complete_warning' : 'Please confirm that this session of self-evaluation has been completed by clicking here. It will generate a comprehensive report. Before any changes to other reports can be made, the confirmation is required. You may also amend the report in the future after confirmation.'
    }
    
    return render(request, 'evaluation/thanks.html', context = context)


@login_required
def report(request, slug):
    #essential part where login_required
    
    null_session(request) 
    #as report marked as completed in the thank you page it is no more required, so that it will let edit the page.
    request.session['evaluator'] = ''
    
    
    
    #as report completed om the thank you page question and total_question no more required.
    try:        
        del request.session['question']
        del request.session['total_question']            
    except KeyError:
        pass

    #only creator can can ccess the report now.
    if request.user.is_producer:
        try:
            get_report = Evaluator.objects.get(slug = slug, creator = request.user)
        except:
            raise PermissionDenied 
    #staff and superuser can access the report               
    elif request.user.is_staff or request.user.is_superuser:
        get_report = Evaluator.objects.get(slug = slug)
    else:
        raise PermissionDenied
    
    
    
    
    #genarating PDF . Please ensure django-xhtml2pdf==0.0.4 installed
    evaluation = Evaluation.objects.filter(evaluator = get_report)
    eva_label = EvaLabel.objects.filter(evaluator = get_report).order_by('sort_order')
    eva_statment = EvaLebelStatement.objects.filter(evaluator = get_report).order_by('pk')
    
    
    
    
    # get ordered next activities
    next_activities = NextActivities.objects.all().order_by('priority')    
    # get common label which is executive summary
    common_label = eva_label.get(label=DifinedLabel.objects.get(common_status = True))
    #delete any prevous record for this current report
    try:
        EvaLebelStatement.objects.filter(evalebel = common_label, evaluator =  get_report, next_activity = True).delete()        
    except:
        pass   
    
    '''
    ========
    part of next activitis started
    ========
    '''
    # to get percentage of related question answered we will make set
    questions_of_report = set()   
    for es in eva_statment:    
        # dont know question will not consider as answere    
        if es.question and not es.dont_know:            
            questions_of_report.add(es.question)    
    # As we are going to enter in the database's next_step field and will be retrive accordingly and diferent label have diferent type of statement we will push the headeing from here.
    summery_statement_next_activities = EvaLebelStatement(evalebel = common_label, next_step = '<b>The following is the prioritised list of validation activities that should be undertaken based on your self assessment responses:</b> <ol>',  evaluator =  get_report, next_activity = True)   
    summery_statement_next_activities.save()
    
    for na in next_activities: 
        
        #geting perchantage
        related_questions = set(na.related_questions.all())
        compulsory_questions = set(na.compulsory_questions.all())
        rel_ques_pecent_in_report = round(len(questions_of_report.intersection(related_questions))/len(related_questions)*100, 2)
        com_ques_percent_in_report = round(len(questions_of_report.intersection(compulsory_questions))/len(compulsory_questions)*100, 2)        
        
        try:  
            #if exist we will edit the percentage only      
            eva_ac = EvaluatorActivities.objects.get(evaluator=get_report, next_activity=na)            
            eva_ac.related_percent = rel_ques_pecent_in_report
            eva_ac.compulsory_percent = com_ques_percent_in_report 
            eva_ac.save()            
        except:  
            #otherwise will be created new.                    
            eva_ac = EvaluatorActivities.objects.create(evaluator=get_report, next_activity=na, related_percent = rel_ques_pecent_in_report, compulsory_percent = com_ques_percent_in_report ) 
        
        # as we need 3 type of result we will take help of memory to change change bool atribute
        if int(eva_ac.related_percent) >= int(na.related_percent) and int(eva_ac.compulsory_percent) >= int(na.compulsory_percent):            
            setattr(na, 'is_active', 'Completed')  
        elif int(eva_ac.related_percent) < int(na.related_percent) and int(eva_ac.related_percent) > 0 and int(eva_ac.compulsory_percent) >= int(na.compulsory_percent):
            setattr(na, 'is_active', 'Not Completed')  
        elif int(eva_ac.related_percent) <= 0:  
            #if 0 we will consider not started becoz if it is touched any percentage can be set.          
            setattr(na, 'is_active', 'Not Started')                         
        else:
            pass     
        
       
        # we will take which is not completed    
        if na.is_active != 'Completed':  
            if int(EvaLebelStatement.objects.filter(evalebel = common_label, evaluator =  get_report, next_activity = True).count()) <= 4:  
                #This is top 5 next activity to the executive summary to save memory space.  
                summery_statement_next_activities = EvaLebelStatement(evalebel = common_label, next_step = f"<li> <p> <b> {str(na.name_and_standared)}({na.is_active}) </b> </p> <p> Short Description: {str(na.short_description)} </p> </li>",  evaluator =  get_report, next_activity = True)    
                summery_statement_next_activities.save() 
            else:
                pass
        else:
            pass
        
        
    # like heading we will puch fotter as well from here    
    summery_statement_next_activities = EvaLebelStatement(evalebel = common_label, next_step ='</ol> <p>PLEASE SEE THE "Deatils of activities" SECTION FOR MORE DETAILS.</p>',  evaluator =  get_report, next_activity = True)
    summery_statement_next_activities.save()   
    '''
    ========
    part of next activitis end
    ========
    '''
    
    
   
    

    context = {
        'evaluation': evaluation,
        'current_evaluator': get_report,
        'eva_label': eva_label,
        'eva_statment': eva_statment,
        'next_activities' : next_activities
    }

    resp = HttpResponse(content_type='application/pdf')
    #below line can help you to find out how to let system decide named report. Just for reference.
    # resp['Content-Disposition'] = 'attachment; filename=Client_Summary.pdf'
    result = generate_pdf( 'evaluation/report.html', context = context, file_object=resp)
    return result










