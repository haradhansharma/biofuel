import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import urlparse
from . nreport_class import ReportPDFData
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
import requests
from .forms import *
from .models import *
from accounts.models import User, UserType
from django.contrib import messages
from django.urls import reverse
from django_xhtml2pdf.utils import generate_pdf
from . helper import (
    get_all_questions,
    get_current_evaluator,
    nreport_context,
    get_picked_na,
    get_all_stdoils,
    get_all_glosaries,
    LabelWiseData,
    get_all_definedlabel,
    get_all_reports_with_last_answer,
    EvaLebelStatementAnalyzer
    
    )
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from accounts.decorators import producer_required, report_creator_required, creator_or_consumer_requried
from gfvp import null_session
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.utils import timezone
import ast

import io  
from django.http import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
import re

from doc.doc_processor import site_info
from django.core.cache import cache

import logging
log =  logging.getLogger('log')


def set_evaluation(question, selected_option, evaluator):
    """
    Set the evaluation for a given question and evaluator.

    This function is intended to be used within the context of the @login_required and @producer_required decorators.

    Parameters:
    - question (Question): The question being evaluated.
    - selected_option (Option): The selected option by the evaluator.
    - evaluator (User): The user performing the evaluation.

    Returns:
    None

    Raises:
    None

    Comments:
    - This function first attempts to delete any previous evaluation entry for the given question and evaluator combination.
    - If no previous evaluation entry is found, it logs a message indicating so.
    - Then, it creates a new evaluation entry with the provided information and saves it to the database.

    Example Usage:
    @login_required
    @producer_required
    def some_view(request, question_id, selected_option_id):
        # Retrieve the Question, Selected Option, and Evaluator
        question = get_question_by_id(question_id)
        selected_option = get_option_by_id(selected_option_id)
        evaluator = request.user

        # Set the evaluation for the given question and evaluator
        set_evaluation(question, selected_option, evaluator)
    """
    try:
        log.info('Deleting previous Evaluation Entry...........')
        # Delete any previous evaluation entry for the same question and evaluator
        Evaluation.objects.filter(evaluator = evaluator, question = question).delete()         
    except:
        log.info(f'No Previous Evaluation entry found for the question {question.id} of the evaluator {evaluator} to delete!')
        
    # Create a new evaluation entry with the provided information
    new_evaluation = Evaluation(evaluator = evaluator, option = selected_option, question = question ) 
    new_evaluation.save()

        
def set_eva_comments(question, comment, evaluator):  
    """
    Set evaluation comments for a given question and evaluator.

    This function is intended to be used within the context of the @login_required and @producer_required decorators.

    Parameters:
    - question (Question): The question for which comments are being set.
    - comment (str): The evaluation comments to be set.
    - evaluator (User): The user (evaluator) providing the comments.

    Returns:
    None

    Raises:
    None

    Comments:
    - This function checks whether an evaluation comment for the given question and evaluator already exists.
    - If a comment entry exists, it updates the comment if a new comment is provided.
    - If no comment entry exists or if the provided comment is empty, it logs a message and creates a new comment entry.

    Example Usage:
    @login_required
    @producer_required
    def add_comment(request, question_id, comment_text):
        # Retrieve the Question and Evaluator
        question = get_question_by_id(question_id)
        evaluator = request.user

        # Set the evaluation comments for the given question and evaluator
        set_eva_comments(question, comment_text, evaluator)
    """
    # Check if an evaluation comment entry already exists for the same question and evaluator
    evacomments = EvaComments.objects.filter(evaluator = evaluator, question = question)
    
    # Ensure that a new comment is provided (non-empty)
    if evacomments.exists():        
        #Ensure new comments
        if comment != '':
            com = evacomments[0]
            com.comments = comment
            com.save()     
    else:
        log.info('No previous comments found!')
        new_eva_comment = EvaComments(evaluator = evaluator, question = question, comments = comment)
        new_eva_comment.save()
        log.info(f'Saved comments for the question {question.id} for the evaluator {evaluator}! ')
        
#helper function should be called into the @login_required and @producer_required    
def set_evastatment(request, selected_option, evaluator):  
    """
    Set evaluation statements for a selected option and evaluator.

    This function is intended to be used within the context of the @login_required and @producer_required decorators.

    Parameters:
    - request: The HTTP request object.
    - selected_option (Option): The selected option for which statements are being set.
    - evaluator (User): The user (evaluator) providing the statements.

    Returns:
    None

    Raises:
    None

    Comments:
    - This function is responsible for setting evaluation statements for a selected option and evaluator.
    - It begins by deleting any previous records of non-assessment statements for the same option and evaluator.
    - It then retrieves the labels associated with the question and sets statements for each label.
    - For each label, it creates a new EvaLebelStatement entry with calculated assessment statements for "don't know" and "positive" answers.
    - It also deletes any previous records of assessment statements for the same label and evaluator.
    - Finally, it logs the completion of the process.

    Example Usage:
    @login_required
    @producer_required
    def set_statements(request, selected_option_id):
        # Retrieve the Selected Option and Evaluator
        selected_option = get_selected_option_by_id(selected_option_id)
        evaluator = request.user

        # Set evaluation statements for the selected option and evaluator
        set_evastatement(request, selected_option, evaluator)
    """
    # Extract the question associated with the selected option  
    question = selected_option.question      
    
    # Delete previous records of non-assessment statements for the same option and evaluator
    try:
        EvaLebelStatement.objects.filter(question = question, evaluator = evaluator, assesment = False).delete()   
    except:
        log.info(f'No previous EvalebelStatement found to delete for the option {selected_option} under question {question.id} of evaluator {evaluator} !')
        
        
    # Retrieve labels associated with the question
    set_labels = Label.objects.filter(question =  question, value = 1) 
    
    for set_label in set_labels:
        # Retrieve the evaluator's EvaLabel for the current label
        eva_label = EvaLabel.objects.get(label__name = set_label.name, evaluator = evaluator)
        
        # Create a new EvaLebelStatement entry for non-assessment
        new_evalebel_statement = EvaLebelStatement(
            evalebel = eva_label, 
            option_id = selected_option.id, 
            statement = selected_option.statement, 
            next_step = selected_option.next_step, 
            dont_know = selected_option.dont_know, 
            question = selected_option.question, 
            positive = selected_option.positive, 
            evaluator =  evaluator)
        new_evalebel_statement.save()
  
        try:
            # Delete previous records of assessment statements for the same label and evaluator
            EvaLebelStatement.objects.filter(
                evalebel = eva_label, 
                evaluator = evaluator, 
                assesment = True).delete()     
            log.info(f'Deleted evalebelstatment which was saved by assesment for evaluator {evaluator} !')       
        except Exception as e:            
            log.info('No assesmented evalabelstatent found to delete! ')
        
        # Calculate assessment statements based on answers and save them
        assesment = EvaLebelStatementAnalyzer(eva_label, evaluator)
        
        # Save the assessment statement for "don't know" answer
        summery_statement_do_not_know = EvaLebelStatement(
            evalebel = eva_label, 
            statement = assesment.label_assesment_for_donot_know(),  
            evaluator =  evaluator, 
            # question = question,  
            assesment = True)
        summery_statement_do_not_know.save()        
        log.info(f'Saved new EvaLebelStatement for "don\'t know" answer for the label {eva_label}')

        # Save the assessment statement for "positive" answer 
        summery_statement_positive = EvaLebelStatement(
            evalebel = eva_label, 
            statement = assesment.label_assesment_for_positive(),  
            evaluator = evaluator,          
            assesment = True)
        summery_statement_positive.save()
        log.info(f'Saved new evalebelstatement for positive answer for the label {eva_label}')
        
    log.info(f'set_evalabelstatement completed for the question {question.id} ! ')
        
def get_eoi(eva_statement):
    '''
    Make as it is optionset have saved in database.
    '''
    es_option_id = set()
    for es in eva_statement:
        if es.option_id is not None:
            es_option_id.add(es.option_id)
    eoi = list(sorted(es_option_id))     
    return eoi     
        
#helper function should be called into the @login_required and @producer_required       
def set_evastatement_of_logical_string(request, selected_option, evaluator):    
    log.info(f'initializing set_evastatement_of_logical_string for evaluator {evaluator} ')
    #review and revise the logical string
    '''
    Making option set based on logical string
    As it is based on multi logicalSting so It can be more hactic to call from signal. or it can be called from cronjob.
    Cronjob can be implemented later to reduce the process load during adding option to the report.
    So Each time of option submitting, we will check if anychange in logicalStrngs and will edit optionset acordingly.
    Then wil be comitted to the report.     
    '''
    log.info('Collecting saved logical strings from the admin backend!')
    logical_strings = LogicalString.objects.all()
    log.info(f'{logical_strings.count()} saved logical strings found! ')    

    
    #make a list of selected_options for each logical strings
    logical_options = [ls_option.option_list for ls_option in logical_strings]  
    
    #geting common lebel
    eva_label_common = EvaLabel.objects.get(label__common_status = True, evaluator = evaluator)
    
    #delete any prevous record for this current report of common label
    try:
        # log.info(f'deleting assesment of common label if any.......')
        EvaLebelStatement.objects.filter(
            evalebel = eva_label_common, 
            evaluator =  evaluator, 
            assesment = True).delete()    
    except Exception as e:
        log.warning(f'Assement deleting was not possible due to {e} !')
    
    assesment = EvaLebelStatementAnalyzer(eva_label_common, evaluator)
    #This is a calculated assesment based on the answere. Called function gives the idea.    
    log.info(f'Recording donot_know_assesment for common label based on answer for report {evaluator} !')
    summery_statement_do_not_know = EvaLebelStatement(
        evalebel = eva_label_common, 
        statement = assesment.overall_assesment_for_donot_know(),  
        evaluator =  evaluator, 
        assesment = True)
    summery_statement_do_not_know.save()
    
    #This is a calculated assesment based on the answere. Called function gives the idea.    
    log.info(f'Recording positive_assement for common label based on answer for report {evaluator}!')
    summery_statement_positive = EvaLebelStatement(
        evalebel = eva_label_common, 
        statement = assesment.overall_assesment_for_positive(),  
        evaluator =  evaluator, 
        assesment = True)
    summery_statement_positive.save()
    
    #get statements of this evaluator
    eva_statement = EvaLebelStatement.objects.filter(evaluator = evaluator) 
    
    #get sorted eoi list to check later
    log.info(f'geting option_id list of evaluation which is name as eoi')
    eoi = get_eoi(eva_statement)

    try:
        
        # log.info(f'Recording logical statment based on eoi to put into the each label of the report {evaluator} ')          
        logical_statement = OptionSet.objects.get(option_list = eoi)
        
        # Check and set to the summary.
        # log.info(f'Setting logical statement to the common label based on answered question to the report {evaluator} !')
        if (str(eoi) in logical_options) and (logical_statement.overall == str(1)):
            try:
                # log.info(f'Deleting previous logical string record in the common label!')
                EvaLebelStatement.objects.filter(
                    evalebel = eva_label_common, 
                    evaluator =  evaluator, 
                    positive = logical_statement.positive).delete()                
            except Exception as e:
                log.info(f'No logical string record found in common label for the eoi!')
            # log.info(f'Saving logical statement to the common label based on the eoi to the report {evaluator} ')
            new_evalebel_statement_common = EvaLebelStatement(
                evalebel = eva_label_common, 
                statement = logical_statement.text, 
                evaluator =  evaluator, 
                positive = logical_statement.positive)
            new_evalebel_statement_common.save()
            
            
        # Check and set to the specific label.  
        # log.info(f'setting logical stement to the each label for the report {evaluator} !')  
        if (str(eoi) in logical_options) and (logical_statement.overall == str(0)):
            log.info(f'eoi found in the logical options')
            ls_id = logical_statement.ls_id
                    
            ls_labels = Lslabel.objects.filter(logical_string__id = ls_id, value = 1)            
            # log.info(f'total {ls_labels.count()} Label found to add logical string for the eoi in the report {evaluator} ')
            for ls_label in ls_labels:                          
                ls_eva_label = EvaLabel.objects.get(label__name = ls_label.name, evaluator = evaluator)                
                try: 
                    # log.info(f'Deleting previous record for this eoi label. ')                    
                    EvaLebelStatement.objects.filter(evalebel = ls_eva_label, evaluator =  evaluator, positive = logical_statement.positive,).delete()                    
                except Exception as e:
                    log.info(f'Not able to delete previous record for the {e} ')   
                # log.info(f'Saving new logical string record for the label {ls_label} ') 
                new_evalebel_statement_g = EvaLebelStatement(
                    evalebel = ls_eva_label, 
                    statement = logical_statement.text, 
                    evaluator =  evaluator, 
                    positive = logical_statement.positive)
                new_evalebel_statement_g.save()  
        else:
            log.info(f'eoi not found in the logical options')          
    except Exception as e:     
        log.info(f'There was problem in recording logical string due to {e} ............................')
    
    #Statement of the option will be aded to the summary if overall is set to 1    
    # log.info(f'Recording statement of the selected option to the common label. ')
    if selected_option.overall == str(1):
        try:
            # log.info(f'deleting previous statement form the common label for this selected option')
            EvaLebelStatement.objects.filter(evalebel = eva_label_common, evaluator =  evaluator, assesment = False).delete()
        except Exception as e:
            log.info(f'There was a problem in deleting previous rrecord due to {e} ')
        log.info(f'Saving record to the common label for the selected option1')
        new_evalebel_statement_common = EvaLebelStatement(
            evalebel = eva_label_common, 
            option_id = selected_option.id, 
            statement = selected_option.statement, 
            evaluator =  evaluator)
        new_evalebel_statement_common.save()    
    
        
        
@login_required
def option_add2(request):    
    log.info(f'Option adding by_____________ {request.user}')
    #as report session can not be started without authenticated user
    try:
        Evaluator.objects.get(id = request.session['evaluator'])
    except:
        messages.warning(request, "What you're trying to do isn't a good idea, please start from begiing!")
        log.warning(f'Somebody try tried to access evaluation procedure without login!')
        return HttpResponseRedirect(reverse('evaluation:evaluation2'))   
    
    #essential part for authenticated user where logedin_required
    null_session(request) 
    log.info(f'starting answer and question procedure for {request.user}!')
    
    
    if request.method == 'POST':        
        question_slug = request.POST['slug']    
        
        #checking options from server side, if frontend skipped by anyhow.        
        if 'option_id' not in request.POST:
            log.info(f'Redirecting as no option selected by the user{request.user}')
            messages.warning(request, 'To proceed, please select an option or please go with "submit" process first!')
            return HttpResponseRedirect(reverse('evaluation:eva_question', args=[int(request.session['evaluator']), str(question_slug)]))       
        
           
        option_id = request.POST['option_id'] 
        comment = request.POST['comment']
        
        
        question = Question.objects.get(slug = question_slug)        
        selected_option = Option.objects.get(id = option_id) 
        
        
        # to check feedback of the option and to submit the comments.
        # I was not agree to this part as it consume more resource and which is unnecessary as 
        # I showed the result by tooltips on the frontend
        # But it was requirment.
        if 'get_feedback' in request.POST:
            # with ThreadPoolExecutor(max_workers=2, initializer=django.setup) as executor:
            # save or update by checking existing coments of user of this report is exist.
            log.info(f'Setting eva comments for {get_current_evaluator(request)}____________')
            set_eva_comments(question, comment,  get_current_evaluator(request) )
            #save or update evaluation by checking existing evaluation
            log.info(f'setting evaluation during geting feedback for report {get_current_evaluator(request)}_______________')
            set_evaluation(question, selected_option, get_current_evaluator(request))  
            return HttpResponseRedirect(reverse('evaluation:eva_question', args=[int(request.session['evaluator']), str(question_slug)]))
        
        #check Option Submitted or not on confirming the feedback
        #This is for first time.
     
        try: 
            Evaluation.objects.get(evaluator = get_current_evaluator(request), question = question).option            
        except Exception as e:
          
            log.info(f'Optin not found_______________')
            messages.warning(request, 'To proceed, please select an option or please go with "submit" process first!')
            return HttpResponseRedirect(reverse('evaluation:eva_question', args=[int(request.session['evaluator']), str(question_slug)]))     
        
        
        set_evaluation(question, selected_option, get_current_evaluator(request))
        #control adding or editing
    
        set_evastatment(question, selected_option, get_current_evaluator(request))
        #control adding or editing
         
        set_evastatement_of_logical_string(question, selected_option, get_current_evaluator(request))
            
            
        #try to find next question if not found report will be genarated and the report(Evaluator) will mark as genarated.
        try:  
            # to forward to next question after submitting a question.          
            next_question = selected_option.next_question  
            
            #This will force user to go to the question if trying to access initial page of evaluation.      
            request.session['question'] = next_question.slug    
            log.info(f'Next question found_______')              
        except: 
            log.info(f'Next question not found_____________')           
            #Mark report as genarated. if no next question found and redirect to Thanks page.                  
            evaluator = Evaluator.objects.get(id = request.session['evaluator'])            
            evaluator.report_genarated = True
            evaluator.save()
            log.info(f'report marked as genareted_____')
          
            
            #create history
            log.info(f'Creating history of the report {evaluator}')
            dfd = LabelWiseData(evaluator).picked_labels_dict()             
            ldf =  LabelDataHistory.objects.filter(evaluator = evaluator)             
            today = timezone.now()       
            ldf.filter(created__gte = today).delete()
            LabelDataHistory.objects.create(evaluator = evaluator, items = dfd)
            
                
                
            log.info(f'Redirecting to the thankyou page')
            return HttpResponseRedirect(reverse('evaluation:thanks'))        

        
        #It is for automatic detection where to go to next based on selection of admin
        if 'submit_and_auto' in request.POST:            
            return HttpResponseRedirect(reverse('evaluation:eva_question', args=[int(request.session['evaluator']), next_question.slug]))
        

#To check question button and mark with specific color by template
@login_required
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
    log.info(f'BNuilding question dataset to show in the evaluation question form')
    #sort_order is most important here    
    
    evaluator = get_current_evaluator(request)
    
    stored_questions = Question.objects.filter(is_active = True)
    
    
    #build parentwise shorted question    
    questions = []
    for question in stored_questions:
        if question.is_door == True:
            questions.append(question)            
            questions.extend([child for child in stored_questions if child.parent_question == question])   
    
    # Pul answered record of the current report
    # Cache should not use here
    evaluations = Evaluation.objects.filter(evaluator=evaluator).order_by('id').select_related('question', 'option')
    
    questions_of_report = []
    for evaluation in evaluations:
        questions_of_report.append(evaluation.question)  
    
    
    #set temporary status of questions     
    for question in questions:
        if question in questions_of_report:
            question.stat = 'checked'   
        else:            
            question.stat = 'skipped'        
    
    #modify status after checked
    try:
        stop_index = max([i for i, j in enumerate([question.stat for question in questions]) if j == 'checked'])       
        for question in questions[int(stop_index) + 1:]:          
            if question.stat == 'skipped':            
                # setattr(question, 'stat', 'unchecked')
                question.stat = 'unchecked'    
            else:            
                continue
    except:
        for question in questions:          
            if question.stat == 'skipped':            
                # setattr(question, 'stat', 'unchecked')
                question.stat = 'unchecked'  
            else:            
                continue
       
    option_of_question = {e.question.id: e.option for e in evaluations}    
    
    for question in questions:       
        try:
            if (option_of_question[question.id]).dont_know == True or (option_of_question[question.id]).name == 'No':
                question.stat = 'skipped'
            else:
                continue
        except Exception:            
            continue    
        
    # if parent is skipped
    childs_to_delete = []    
    for question in questions:
        if question.is_door == True and question.stat == 'skipped':
            childs = [child for child in questions if child.parent_question == question]            
            for child in childs:
                setattr(child, 'stat', 'skipped')                
                childs_to_delete.append(child)
    evaluations.filter(question__in = childs_to_delete).delete()               

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
            
    log.info(f'Question dataset build___________')
    return results

def get_vedio_urls(search_term):
    search_url = 'https://www.googleapis.com/youtube/v3/search'     
    params = {
        'part' : 'snippet',
        'q' : search_term,
        'key' : settings.YOUTUBE_DATA_API_KEY,
        'maxResults' : 3,
    }
    r = requests.get(search_url, params=params, )
    search_results = r.json()
    vedio_urls = []
    for item in search_results.get('items'):
        try:
            item_id = item['id']        
            embed_url = 'https://www.youtube.com/embed/{}'.format(item_id['videoId'])
            vedio_urls.append(embed_url)
        except:
            continue
    return vedio_urls


from asgiref.sync import sync_to_async
@sync_to_async
def vedio_urls(request, search_term):
    saved_urls = Youtube_data.objects.filter(term = search_term) 
    if saved_urls.exists():
        log.info(f'Found saved url for youtube video________')
        saved_url = saved_urls[0]
        vedio_urls = ast.literal_eval(saved_url.urls) #convert string list to list
        if (saved_url.update_date + timezone.timedelta(days=7))  < timezone.now():
            saved_url.urls = get_vedio_urls(search_term)
            saved_url.save()         
    else:
        log.info(f'Hiting api for youtube video as no saved video found_______')
        vedio_urls = get_vedio_urls(search_term)        
        Youtube_data.objects.create(term = search_term, urls = vedio_urls)  
    # return vedio_urls  
    return render(request, 'evaluation/eva_youtube.html', context = {'vedio_urls' : vedio_urls})
@sync_to_async
def std_oils_block(request, slug):
    question = Question.objects.prefetch_related('stanchart').get(slug = slug)
    
    return render(request, 'evaluation/std_oils_block.html', context = {'question': question})


@sync_to_async
def quotation_block(request, slug):
    question = get_all_questions().get(slug = slug)
    picked_na = get_picked_na(question)            
    return render(request, 'evaluation/quotation_block.html', context = {'question': question, 'next_activities':picked_na})
    
'''
====
Main interface during evaluation process.
====
'''

@login_required
@producer_required
def eva_question(request, evaluator_id, slug):   
    
    if isinstance(evaluator_id, str): # Check if the parameter is a string
        evaluator_id = int(evaluator_id) # Convert the string to an integer
    
    '''
    Question answering process start here
    :request is current request
    :evaluator_id ID not object. Alternatively it can call Report ID
    :slug is question slug
    ''' 
    
     
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
        log.info(f'Found unusual activity by user {request.user} as he tried to access evaluation process where he is not permitted.')
        messages.warning(request, 'You are not permitted to access the requested webpage!')
        return HttpResponseRedirect(reverse('evaluation:evaluation2')) 
    
    
    
    '''
    if anybody coming from initial page then system will get session evaluator
    if no report is in progress evaluator will be '' . it is ensured by middleware.
    if anybody going to edit report then report id will be taken as session evaluator.
    
    '''   
 
    eva = get_current_evaluator(request, evaluator_id)
    if request.session['evaluator'] == '':
        request.session['evaluator'] = evaluator_id
        # edit_evaluator = eva      
        eva.report_genarated = False
        # log.info(f'As report is being edited so report_genarated set to false________________')
        eva.save()    

            
        
        
    '''
    Below evaluator checking will ensure the correct report are editing.
    Otherwise user will put data by thinking one report but data can be edited in another report. Things can be messy.
     
    ''' 
    if request.session['evaluator'] !=  evaluator_id:      
        log.info(f'Without completing a report trying to edit another report, so it is abroted________')      
        messages.warning(request, f"You have an active, unfinished Report, Report#{request.session['evaluator']}! So you're not permitted to perform this procedure!")        
        return HttpResponseRedirect(reverse('accounts:user_link'))  
    
    

        
    
    '''
    creator can edit own report!
    '''   
  
    if eva.creator.id == request.user.id or request.user.is_superuser or request.user.is_staff:
        pass
    else:
        log.info(f'The report is being edited is not created you user {request.user}______abroating______')
        raise PermissionDenied  
    
    
 
    
    all_questions = get_all_questions()
    question = Question.objects.get(slug = slug)  
    
    evaluator_data = get_current_evaluator(request)
    evaluation_data = Evaluation.objects.filter(evaluator = evaluator_data).select_related('question','option').order_by('id') 
    
    
    
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
        log.info(f'Parent Question Clicked________for report {evaluator_data}_______')      
        pass  
    else:
        parent = question.parent_question
        # evaluations = evaluation_data.filter(evaluator = evaluator_data).order_by('id')  
        evaluations = evaluation_data
        
        questions_of_report = []
        for evaluation in evaluations:
            questions_of_report.append(evaluation.question)
        try:
            get_option = evaluation_data.get(question = parent).option
            if parent not in questions_of_report or get_option.yes_status == False:
                log.info(f'Parent question is not answered as "yes" to go inside of this quesion block_____so abroating to the parent question')
                messages.warning(request, 'To go inside this block, you must answer "Yes" to the specified question!')
                return HttpResponseRedirect(reverse('evaluation:eva_question' ,  args=[int(evaluator_id),  str(parent.slug)]))  
        except:   
            log.info(f'Parent question is not answered as "yes" to go inside of this quesion block_____so abroating to the parent question')                     
            messages.warning(request, 'To go inside this block, you must answer "Yes" to the specified question!')
            return HttpResponseRedirect(reverse('evaluation:eva_question' ,  args=[int(evaluator_id), str(parent.slug)]))  
        
        
                
    
    '''
    The qualified rang can be set from Admin>>Site>>qualified ans rang
    '''
  
    qualified_ans_rang = int(site_info().get('qualified_ans_range'))       
    
    eva_lebels = EvaLabel.objects.filter(evaluator = evaluator_data).order_by('sort_order').prefetch_related('elabelstatement').select_related('label')    
    
    total_evaluation_data = len(evaluation_data)
    request.session['total_question'] = total_evaluation_data
    
    total_ques = len(all_questions) - total_evaluation_data
    timing_text = f"Depending on how many answers you provide, the self assessment will take \
        anywhere from {round(total_ques/10)} to {round(total_ques/3)} minutes. At the end of the \
            assessment, a PDF report will be provided, which can be retrieved via the Dashboard at a later stage."
    
    try:
        submitted_comment = EvaComments.objects.get(evaluator = evaluator_data, question = question).comments
    except:
        submitted_comment = None   
    
    '''
    if previously answered in this report then the option will show as selected.
    if not answered previously and there have a option in the standared oil of this question
    then this option will be selected as default and there will set a attribute named 'robot_data' to show the message
    ''' 
    question_in_evaluation = evaluation_data.filter(question = question) 
    
    try:
        selected_option = question_in_evaluation.get(question = question).option
    except:
        oils = question.stanchart.filter(oil__select_oil__key = evaluator_data.stdoil_key)
        if oils.exists():
            selected_option = oils[0].option if oils[0].option else None
            if selected_option is not None:
                setattr(selected_option, 'robot_data', '(default estimate by reference)')  
        else:
            selected_option = None  
    
    
    # Create push url for HTMX     
 
    if question_in_evaluation is not None:
        try:
            next_question_slug = selected_option.next_question.slug
            request.session['push_url'] = reverse('evaluation:eva_question', args=[int(request.session['evaluator']), next_question_slug])            
        except:
            request.session['push_url'] = reverse('evaluation:thanks')
    else:
        request.session['push_url'] = ''        
    
    
    label_data = LabelWiseData(evaluator_data)
    answered_percent = label_data.answered_percent
  
    '''
    Geting data from youtube data api 
    update data in each week   
     
    '''    
    
    search_term = re.sub('[^A-Za-z0-9]+', ' ',  f'{question.name} {evaluator_data.biofuel.name}')   
    
    # log.info(f'total questions________________{Question.objects.filter(is_active=True).count()}')
    
    

    context ={
        'slug' : slug,
        'question_dataset' : question_dataset(request) ,
        'question': question,
        # 'optns': options,
        'evaluator_data': evaluator_data,
        'eva_lebels': eva_lebels,
        'timing_text': timing_text,    
        'total_question': int(request.session['total_question']), 
        'qualified_rang' : int(qualified_ans_rang),   
        'evaluator':evaluator_id, 
        'selected_option' : selected_option,
        'submitted_comment' : submitted_comment,
        # 'chart_data' : chart_data,
        # 'vedio_urls' : vedio_urls(search_term),
        'search_term' : search_term,
        # 'oil_graph_data' : oil_graph_data,
        'answered_percent' : answered_percent,
        
        
    }
    
    
    #meta
    meta_data = site_info()    
    meta_data['title'] = question.name
    meta_data['description'] = f"Depending on how many answers you provide, the self assessment will take anywhere from 10 to 33 minutes. At the end of the assessment, a PDF report will be provided."
    meta_data['tag'] = 'biofuel, evaluation'
    meta_data['robots'] = 'noindex, nofollow'
    # meta_data['og_image'] = request.user.type.icon.url 
    
    context.update({
        'site_info' : meta_data,  
    })
    
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
    
    
    #rechecking user is authorized or not, although it is not necessary as only logedin user can enter to this page, but it is safe to avoid error if anyhow decorator are removed. 
    
        
    if request.user.is_authenticated:
        usertype = request.user.usertype
        name = request.user.get_full_name() or first_report_name
        email = request.user.email
        phone = request.user.phone
        orgonization = request.user.orgonization
    else:
        usertype = UserType.objects.get(slug=request.session['interested_in'])
        name = ''
        email = ''
        phone = ''
        orgonization = ''
    
    
    #Preparing guard to check whether system should take initial data or need to forwared to next_question of selected question previously.
    # log.info(f'Checking new creating or adding or editing_______')
    try:
        session_evaluator = Evaluator.objects.get(id = request.session['evaluator'])      
    except Exception as e:        
        session_evaluator = False  
        
        
    #get first question of evaluation process based on short_order. If no first question set by admin will redirect to homepage with warning message.
    # log.info(f'Check first question is set or not by admin______________')
    try:
        first_of_parent = Question.objects.filter(is_door = True).order_by('sort_order').first()              
    except:
        # log.info(f'First question has not been set by the admin____________________')
        messages.warning(request,'There is something wrong in procedure setting by site admin, Please try again latter!')
        return HttpResponseRedirect(reverse('evaluation:evaluation2'))   
    
    #Scaning by guard
    if (session_evaluator is False) or ('question' not in request.session):
        log.info(f'Evaluation going to be started by_____________ {request.user}')
        if request.method == "POST": 
            form = EvaluatorForm(request.POST)
            if form.is_valid():            
                ##take data 
                name = form.cleaned_data['name']
                email = form.cleaned_data['email'] 
                phone = form.cleaned_data['phone']
                orgonization = form.cleaned_data['orgonization']
                biofuel = form.cleaned_data['biofuel']
                stdoil_key = request.POST.get('stdoil')    
                make_it_public = form.cleaned_data['make_it_public']
               
          
                #genarate report's initial data. It is a basement of a report or evaluation.
                new_evaluator = Evaluator(
                    creator = request.user, 
                    name = name, 
                    email = email, 
                    phone = phone, 
                    orgonization = orgonization, 
                    biofuel = biofuel, 
                    stdoil_key = stdoil_key,
                    make_it_public = make_it_public                    
                    )
                new_evaluator.save()
                
                #Catch user record from the evaluation form if not exists
                user = request.user
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
                defined_label = get_all_definedlabel()
                for dl in defined_label:
                    new_evalabel = EvaLabel(label = dl, evaluator = get_current_evaluator(request), sort_order=dl.sort_order)
                    new_evalabel.save()            
                return HttpResponseRedirect(reverse('evaluation:eva_question' ,  args=[int(request.session['evaluator']), str(first_of_parent.slug)]))
            else:
                messages.warning(request,'Error in form submission')
                messages.error(request, form.errors)   
                return HttpResponseRedirect(reverse('evaluation:evaluation2'))   
            
        
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
                first_biofuel = None
                first_report_name = ''  
                    
                    
            initial_dict = {
            "usertype" : usertype,
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
        
        new_report = request.session['evaluator']
        next_question = request.session['question']
        if 'question' in request.session:
            log.info(f' Going to the next question {next_question} of the report {new_report}_________')
            return HttpResponseRedirect(reverse('evaluation:eva_question', args=[int(new_report), str(next_question)]))
        else:            
            log.info(f'Report {new_report} being started with the first qestion {first_of_parent}______________')
            return HttpResponseRedirect(reverse('evaluation:eva_question' ,  args=[int(new_report), str(first_of_parent.slug)]))
            
    total_ques = get_all_questions().count()
    box_timing = f"Please note that the duration of the self-assessment may vary depending on the number of questions you are required to answer. n\
    Typically, it can take between {round(total_ques/10)} to {round(total_ques/3)} minutes to complete. Once the assessment is finished, n\
    you will receive a PDF report, which is also accessible through your profile."
        

    
    
    # stdoil_list = StandaredChart.objects.filter(related_biofuel = first_biofuel).values('oil_name', 'key').order_by('oil_name').distinct()
    
    stdoil_list = get_all_stdoils().filter(biofuel = first_biofuel)
    
    
    #meta
    meta_data = site_info()    
    meta_data['title'] = 'Evaluation Index, starting point of evaluation process!'
    meta_data['description'] = f"This is the starting point of biofuel evaluation process at green fuel validation platform. Here producer need to give authority information to start validation process!"
    meta_data['tag'] = 'biofuel, evaluation'
    meta_data['robots'] = 'noindex, nofollow'
    # meta_data['og_image'] = request.user.type.icon.url 
    
    context ={
        'form': form,
        'box_timing': box_timing, 
        'stdoil_list' : stdoil_list,
        'site_info' : meta_data,          
    }   
    
    return render(request, 'evaluation/new_index.html', context = context)




    
   
@login_required
@producer_required    
def thanks(request):   
    
    #essential part where login_required
    null_session(request)  
    log.info(f'Thank you page accessed by_____________ {request.user}')
    '''
    Deletion of incomplete report are not necessary , if need can uncomments below code. need to check if raising any error.As an incomplete report may not have evalauation or statment both.
    '''  
    producer_slug = UserType.objects.filter(Q(name__icontains='producer') | Q(slug__icontains='producer')).first().slug
    
    try:        
        last_reports = get_current_evaluator(request)        
    except:
        last_reports = None    
    
    #Session evaluator is most important to view calculated result in the thankyou page.
    #By default session's null evaluator has been created by middlewear
    if request.session['evaluator'] == '':        
        return HttpResponseRedirect(reverse('accounts:user_link'))
    
    # evaluator =  get_current_evaluator(request)
    #Calculation to display on the thankyou page.
    label_data = LabelWiseData(last_reports)   
    
    ans_ques = len(label_data.answered_question_id_list)
    dont_know_ans = ans_ques - label_data.total_positive_answer - label_data.total_nagetive_answer
    pos_ans = label_data.total_positive_answer
    positive_percent = label_data.overview_green
    dont_know_percent = label_data.overview_grey
    
    
     
    gretings = 'Thank you very much! Your information has been saved!'
    button = f"{reverse('evaluation:nreport', args=[last_reports.slug])}"+"?confirm=confirm" 
    
    '''
    Build all report editing url
    Parent should be selected by admin otherwise site can arise error. 
    '''
    #increadable setattr to reduce time to make report editing url without touch of database    
    
    try:             
        first_of_parent = get_all_questions().filter(is_door=True).order_by('sort_order').first()
    except:
        messages.warning(request,'There is something wrong in procedure setting by site admin please try again latter!')
        return HttpResponseRedirect(reverse('evaluation:evaluation2'))        
    
    # Pagination shold be implemented
    reports = get_all_reports_with_last_answer(request, first_of_parent)
    
    #Paginated response
    page = request.GET.get('page', 1)
    paginator = Paginator(reports, 10)
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        reports = paginator.page(1)
    except EmptyPage:
        reports = paginator.page(paginator.num_pages)
    
    #meta
    meta_data = site_info()    
    meta_data['title'] = 'Thank you'
    meta_data['description'] = f"This is the thank you page afte evaluation process completed. Here, registerd user can view his information and created reports. Also Can go to the profiel setting page."
    meta_data['tag'] = 'thank you, gf-vp.com'
    meta_data['robots'] = 'noindex, nofollow'
    meta_data['og_image'] = request.user.usertype.icon.url 

    context = {
        'donotshow' : 'yes',
        'site_info' : meta_data,
        'refferer_path' : urlparse(request.META.get('HTTP_REFERER')).path,
        'gretings': gretings,
        'button': button,
        'ans_ques': ans_ques,
        'dont_know_ans': dont_know_ans,
        'pos_ans': pos_ans,
        'positive_percent': str("%.2f" % positive_percent) + '%',
        'dont_know_percent': str("%.2f" % dont_know_percent) + '%',
        'reports': reports,
        'last_reports' : last_reports,
        'producer_slug' : producer_slug,
        'complete_report_button_text': 'Confirm and Generate',
        'complete_warning' : 'Please confirm that this session of self-evaluation has been completed by clicking here. n\
            It will generate a comprehensive report. Before any changes to other reports can be made, the confirmation is n\
                required. You may also amend the report in the future after confirmation.'
    }
    
    return render(request, 'evaluation/thanks.html', context = context)


def trafic_light_hori(request, last_reports):
    report = Evaluator.objects.get(id = last_reports)
    label_data = LabelWiseData(report)
    df = label_data.packed_labels()      
    item_label = df.columns.values.tolist()
    item_seris = df.values.tolist()
    context = {
        'item_label' : item_label,
        'item_seris' : item_seris,
        'report' : report
    }
    return render(request, 'evaluation/tl_hori.html', context = context)


def fuel_history(request, last_reports):
    report = Evaluator.objects.get(id = last_reports)
    label_data = LabelWiseData(report)
    dfh = label_data.label_data_history()         
    # item_label = df.columns.values.tolist()
    # item_seris = df.values.tolist()
    context = {
        'dfh' : dfh,
        
        
    }
    return render(request, 'evaluation/fuel_history_chart.html', context = context)
    


@login_required
@creator_or_consumer_requried
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

    #As we are checking the function with decorator then we can query the report directly  
    try:  
        get_report = Evaluator.objects.get(slug = slug)
    except:
        messages.warning(request, 'No report found!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  
    
    
    #genarating PDF . Please ensure django-xhtml2pdf==0.0.4 installed
    evaluation = Evaluation.objects.filter(evaluator = get_report)
    eva_label = EvaLabel.objects.filter(evaluator = get_report).order_by('sort_order')
    eva_statment = EvaLebelStatement.objects.filter(evaluator = get_report).order_by('pk')
    
    
    # get ordered next activities
    next_activities = NextActivities.objects.all().order_by('priority')    
    # get common label which is executive summary    
    common_label = eva_label.get(label__common_status = True)
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

    na_ac = []    
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
    
        if na.is_active != 'Completed':  
            if len(na_ac) <= 5:
                na_ac.append(na)
            else:
                break
        else:
            continue
        

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
        'next_activities' : next_activities,
        'na_ac' : na_ac,
        
    }

    resp = HttpResponse(content_type='application/pdf')
    #below line can help you to find out how to let system decide named report. Just for reference.
    # resp['Content-Disposition'] = 'attachment; filename=Client_Summary.pdf'
    result = generate_pdf( 'evaluation/report.html', context = context, file_object=resp)
    return result

from crm.models import ConsumerMailQueue
def create_notification_to_consumer(report):
    consumers = User.objects.filter(usertype__is_consumer = True, is_active = True)    
    # Assuming you have a list of consumers with emails
    consumer_emails = [consumer.email for consumer in consumers if consumer.ns.new_fuel_notifications]
    # Create a list of ConsumerMailQueue instances
    consumer_mail_queues = [
        ConsumerMailQueue(to=email, report=report) for email in consumer_emails
    ]

    # Bulk insert the instances into the database
    ConsumerMailQueue.objects.bulk_create(consumer_mail_queues)
    
    return None
               


@login_required
@creator_or_consumer_requried
def nreport(request, slug): 
    #essential part where login_required    
    null_session(request)         
    
    context = nreport_context(request, slug)  
    
    report = context['current_evaluator']
    
    
    # if report creating or editing
    if 'confirm' in request.GET:
        create_notification_to_consumer(report)
        
    #meta
    meta_data = site_info()    
    meta_data['title'] = f'Analysis Report #{report.id}'
    meta_data['description'] = f"Green fuel validation platform-Analysis Report."
    meta_data['tag'] = 'Analysis Report, gf-vp.com'
    meta_data['robots'] = 'noindex, nofollow'
    meta_data['og_image'] = request.user.usertype.icon.url 
    
    
    context.update({
        'site_info' : meta_data,
    })
    
    return render(request, 'evaluation/nreport.html', context = context)   

        
@login_required
@creator_or_consumer_requried       
def nreport_pdf(request, slug):
    '''
    new df report based on reportlab
    '''
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)   
    rpf = ReportPDFData(request, slug)
    
    doc.leftMargin = rpf.M
    doc.rightMargin = rpf.M   
    doc.topMargin = rpf.M
    doc.bottomMargin = rpf.M
    doc.pagesize = rpf.pagesize
    
    title = f'EVALUATION REPORT OF {rpf.evaluator().biofuel.name.upper()}--#{rpf.evaluator().id}'
    
    doc.title = title
    doc.author = rpf.author    
    doc.creator = rpf.creator    
    doc.producer = rpf.producer
    
    author = Paragraph(rpf.author, rpf.Footer)
    creator = Paragraph(rpf.creator, rpf.Footer)   
    producer = Paragraph(rpf.producer, rpf.Footer)
    
    
    Story = rpf.wrapped_pdf()
    Story.append(PageBreak())
    Story.append(Spacer(rpf.PH/2,rpf.PH/2))    
    Story.append(rpf.ulineDG100())
    Story.append(Paragraph('<a name = "on"/><b>:Author:</b>', rpf.Footer))
    Story.append(author)
    Story.append(Paragraph('<b>:Creator:</b>', rpf.Footer))    
    Story.append(creator)
    Story.append(Paragraph('<b>:Producer:</b>', rpf.Footer))    
    Story.append(producer)
    Story.append(Spacer(0.25*inch,0.25*inch))   
    Story.append(Paragraph('<b>:::::::::::::::::THE END::::::::::::::::::</b>', rpf.Footer))    
     
       
    doc.build(Story, onFirstPage=rpf.first_page, onLaterPages=rpf.later_page)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=title + '.pdf')

def stdoils(request):
    biofuel_id = request.GET.get('biofuel')    

    stdoil_list = get_all_stdoils().filter(biofuel__id = biofuel_id)     
    return render(request, 'evaluation/std_oils.html', {'stdoil_list' : stdoil_list})


def get_glossary(request):    
    return render(request, 'glossary/glossary_template.html', {'object_list' : get_all_glosaries()})

@report_creator_required
def edit_report(request, slug):   
    report = get_object_or_404(Evaluator, slug=slug) 
    form = EvaluatorEditForm(instance=report)
    if request.method == 'POST':    
        form = EvaluatorEditForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            
        return HttpResponseRedirect(reverse('home:all_reports'))
        
    context = {
       'form' : form 
    }
    return render(request, 'home/edit_report.html', context)
    




