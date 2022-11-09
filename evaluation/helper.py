from .models import *
from django.utils import timezone
from django_cron import CronJobBase, Schedule
import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from doc.doc_processor import site_info
from gfvp import null_session
from django.contrib.sites.shortcuts import get_current_site

import logging
log =  logging.getLogger('log')



def active_sessions():
    '''
    we will collect all active session's evaluator id of before past 24 hours
    it returns list
    '''
    from django.contrib.sessions.models import Session # As it is sensative operation I will call it inside this function only.
    sessions = Session.objects.filter(expire_date__gt = (timezone.now() - timezone.timedelta(hours=24)))
    s_evs = set()
    for s in sessions:
        s_data = s.get_decoded()
        try:
            eva = s_data.get('evaluator')
        except:
            eva = None
        if eva:
            s_evs.add(s_data.get('evaluator'))
    # log.info(f"Collected active session's evaluator id set, which is {s_evs}")
    return list(s_evs)

def clear_evaluator():
    '''
    IT IS RUNNING BY CRON JOB
    we will remove all wastage report which just initialized but have no data and which is not qualified to show in the profile page.
    It returns total deleted report in a call.
    It is created to call by CRONJOB but can be called from anywhere.
    
    '''
    evaluator = Evaluator.objects.filter(report_genarated = False) 
    total_deleted = 0
    if evaluator.exists():
        try:
            for e in evaluator:                
                if e.id not in active_sessions(): # to avoid deleting running session's evaluator
                    if e.eva_evaluator.count() == 0: # as first related data is beeing saving into the evaluation table so that we will check these table only.
                        Evaluation.objects.filter(evaluator = e).delete()
                        EvaLebelStatement.objects.filter(evaluator = e).delete()                
                        EvaLabel.objects.filter(evaluator = e).delete()
                        EvaComments.objects.filter(evaluator = e).delete()                
                        Evaluator.objects.filter(id = e.id).delete()
                        log.info(f'Report {e} with related data from Evaluation, EvaLabelStatement, EvaLabel, EvaComments, Evaluator has been deleted due t no record to the related tables!')   
                        total_deleted += 1             
        except Exception as e:
            log.warning(f'error {e} happend while deleteing incomplete report!')
            
    # log.info(f'{total_deleted} incomplete report has been deleted!')
    return total_deleted

    


def get_current_evaluator(request):
    evaluator = Evaluator.objects.get(id = request.session['evaluator'])
    return evaluator

def ans_to_the_label(evalebel, evaluator):
    ans_to_the_label = EvaLebelStatement.objects.filter(evalebel = evalebel, evaluator = evaluator, question__isnull = False, assesment = False).values('evalebel').distinct().count()
    return ans_to_the_label
    

#calculated statement genarator for report, is called in evaluatin procedure. function name telling what is being calulated
def label_assesment_for_donot_know(request, evalebel, evaluator):
    'label wise Sumamry'
    # ans_to_the_label = EvaLebelStatement.objects.filter(evalebel = evalebel, evaluator = evaluator, question__isnull = False, assesment = False).values('evalebel').distinct().count()
    dont_know_ans_to_the_lebel = EvaLebelStatement.objects.filter(evalebel = evalebel, evaluator = evaluator, question__isnull = False, dont_know = 1, assesment = False).values('evalebel').distinct().count()
    dont_know_percent_to_the_label = (int(dont_know_ans_to_the_lebel) * 100)/int(ans_to_the_label(evalebel, evaluator))
    
    if dont_know_percent_to_the_label < 20:
        statement = str(evalebel.label.name) + ' assessment of your biofuel shows that you have very detailed knowledge.'
    elif dont_know_percent_to_the_label < 35:
        statement = str(evalebel.label.name) + ' assessment of your biofuel shows that you have very significant knowledge.'
    elif dont_know_percent_to_the_label < 50:
        statement = str(evalebel.label.name) + ' assessment of your biofuel shows that you have very limited knowledge.'
    else:
        statement = str(evalebel.label.name) + ' assessment of your biofuel shows that you have very rudimentary knowledge.'

    return statement

#calculated statement genarator for report, is called in evaluatin procedure. function name telling what is being calulated
def label_assesment_for_positive(request, evalebel, evaluator):
    'label wise Sumamry'
    # ans_to_the_label = EvaLebelStatement.objects.filter(evalebel = evalebel, evaluator = evaluator, question__isnull = False, assesment = False).values('evalebel').distinct().count()
    pos_ans_to_the_lebel = EvaLebelStatement.objects.filter(evalebel = evalebel, evaluator = evaluator, question__isnull = False, positive = 1, assesment = False).values('evalebel').distinct().count()
    positive_percent_to_the_label = (int(pos_ans_to_the_lebel) * 100)/int(ans_to_the_label(evalebel, evaluator))
    
    if positive_percent_to_the_label < 50:
        statement = 'Based on the response to the enquiry, the ' + str(evalebel.label.name).lower() + ' evaluation of your oil contains multiple serious shortcomings.'
    elif positive_percent_to_the_label < 75:
        statement = 'According to the response to the query, the ' + str(evalebel.label.name).lower() + ' evaluation of your oil is generally good. However, there are a few shortcomings that needs be addressed further.'
    elif positive_percent_to_the_label < 90:
        statement = 'According to the response to the inquery, the ' + str(evalebel.label.name).lower() + ' evaluation of your oil is largely favourable Nonetheless, the aformentioned issues must be considered in to account.'
    else:
        statement = 'According to the response to the query, the ' + str(evalebel.label.name).lower() + ' evaluation of your oil is highly promising. It has a lot of promise in terms of the ' + str(evalebel.label.adj).lower() + '.'

    return statement

def ans_ques(evaluator):
    ans_ques = EvaLebelStatement.objects.filter(evaluator = evaluator, question__isnull = False, assesment = False).values('question').distinct().count()
    return ans_ques
    

#calculated statement genarator for report, is called in evaluatin procedure. function name telling what is being calulated
def overall_assesment_for_donot_know(request, evalebel, evaluator):
    # ans_ques = EvaLebelStatement.objects.filter(evaluator = evaluator, question__isnull = False, assesment = False).values('question').distinct().count()
    dont_know_ans = EvaLebelStatement.objects.filter(evaluator = evaluator, question__isnull = False, dont_know = 1, assesment = False).values('question').distinct().count()
    dont_know_percent = (int(dont_know_ans) * 100)/int(ans_ques(evaluator))

    if dont_know_percent < 20:
        statement = 'Overall' + ' assessment of your biofuel shows that you have very detailed knowledge.'
    elif dont_know_percent < 35:
        statement = 'Overall' + ' assessment of your biofuel shows that you have very significant knowledge.'
    elif dont_know_percent < 50:
        statement = 'Overall' + ' assessment of your biofuel shows that you have very limited knowledge.'
    else:
        statement = 'Overall'+ ' assessment of your biofuel shows that you have very rudimentary knowledge.'
    return statement

#calculated statement genarator for report, is called in evaluatin procedure. function name telling what is being calulated
def overall_assesment_for_positive(request, evalebel, evaluator):
    # ans_ques = EvaLebelStatement.objects.filter(evaluator = evaluator, question__isnull = False, assesment = False).values('question').distinct().count()
    pos_ans = EvaLebelStatement.objects.filter(evaluator = evaluator, question__isnull = False, positive = 1, assesment = False).values('question').distinct().count()   
    
    positive_percent = (int(pos_ans) * 100)/int(ans_ques(evaluator))
    
    if positive_percent < 50:
        statement = 'Based on the response to the enquiry, the ' + 'overall' + ' evaluation of your oil contains multiple serious shortcomings.'
    elif positive_percent < 75:
        statement = 'According to the response to the query, the ' + 'overall' + ' evaluation of your oil is generally good. However, there are a few shortcomings that needs be addressed further.'
    elif positive_percent < 90:
        statement = 'According to the response to the inquery, the ' + 'overall' + ' evaluation of your oil is largely favourable Nonetheless, the aformentioned issues must be consdered in to account.'
    else:
        statement = 'According to the response to the query, the ' + 'overall' + ' evaluation of your oil is highly promising. It has a lot of promise in terms of the ' + str(evalebel.label.adj).lower() + '.'

    return statement

class OilComparision:
    def __init__(self, oil, non_answered = None):
        self.oil = oil
        
        
        if non_answered is not None:
            self.active_questions = Question.objects.filter(id__in = non_answered, is_active=True)    
        else:
            self.active_questions = Question.objects.filter(is_active=True)    
                 
        self.oils = StandaredChart.objects.filter(oil = self.oil)
       
        
    def total_active_questions(self):
        data = self.active_questions.count()
        return round(data, 2)
    
    def total_positive_options(self):        
        '''
        to get positive question based on pisitive option of the oil
        '''
        data = []
        for oil in self.oils:
            try:
                if int(oil.option.positive) == 1:
                    data.append(oil.option)  
            except:
                continue                
        
        return round(len(data), 2)
    
    def total_negative_options(self):     
        '''
        to get negetive question based on negative options of the oil
        '''   
        data = []
        for oil in self.oils:
            try:                             
                if int(oil.option.positive) == 0:
                    data.append(oil.option)      
            except:
                continue        
             
        return round(len(data), 2)
    
    def overview_green(self):
        data = (self.total_positive_options()/self.total_active_questions())*100        
        return round(data, 2)
    
    def overview_red(self):
        data = (self.total_negative_options()/self.total_active_questions())*100        
        return round(data, 2)
    
    def overview_grey(self):
        '''
        As overview green and overview red is in parcent so we will deduct from 100 the both to equalized dividation in barchart.
        As each question have no label and have multiple positive value or negative value so sum of labelwise questions result is diferent then actual total question.
        For this reason to get rid of the mismatched result we had to deduct from 100 to get matching report in the barchart.        
        '''
        data = 100 - (self.overview_green() + self.overview_red())           
        return round(data, 2)
    
    def total_result(self):
        '''
        As per writen CSS our fist stacked bar will be green, second bar will be grey and third bar will be red so 
        we will placed the value in the list acordingly. We need to decide label name here so that it will be easy to impleted along with labels as each label has predifiened name.
        '''
        record = {
            #green>>grey>>red
            'Overview' : [self.overview_green(), self.overview_grey(), self.overview_red()]
            }
        return record
    
    def label_wise_positive_option(self, label):              
        data = self.oils.filter(question__questions__name = label, option__positive = str(1)).count()        
        return round(data, 2)
    
    def label_wise_negative_option(self, label):              
        data = self.oils.filter(question__questions__name = label, option__positive = str(0)).count()       
        return round(data, 2)
    
    def label_wise_result(self):       
        labels = DifinedLabel.objects.filter(common_status = False)        
        record_dict = {}
        for label in labels:             
            positive = round(self.active_questions.filter(questions__name = label, questions__value = str(1)).count(), 2)       
            #As labelwise record is more then total question due to multi label selected for each question
            #so we will make it based on the total positive       
            positive_options = round((self.label_wise_positive_option(label)/self.active_questions.count())*positive, 2)              
            negative = round(self.active_questions.filter(questions__name = label, questions__value = str(0)).count(), 2)
            # same as positive
            negative_options = round((self.label_wise_negative_option(label)/self.active_questions.count())*negative, 2)       
            green = round((positive_options/positive)*100, 2)
            red = round((negative_options/negative)*100, 2)         
            
            record = {
                #Same as total total result
                #green>>grey>>red
                label.name : [green , round(100-(green+red),2), red]
            }  
            
            record_dict.update(record)         
               
        return record_dict
    
    
    def picked_labels_dict(self):
        label_result = {}    
        label_result.update(self.label_wise_result())
        label_result.update(self.total_result()) 
        return label_result
    
    def packed_labels(self):        
        '''
        From dataframe we will take rows to use in JS's series.
        '''
        df = pd.DataFrame(self.picked_labels_dict())   
        return df  
        


class LabelWiseData:
        
    def __init__(self, evaluator):
        # The evaluator can be either from session or url which will be supplied
        self.evaluator = evaluator   
        # We will neeed total active questions in the site to use by filtering sing diferent parameter     
        self.active_questions = Question.objects.filter(is_active=True)
        # we will need the statment added from the selected options during answering for this report/evaluator, must be excluded assesments or logical strings
        self.eva_label_statement = EvaLebelStatement.objects.filter(evaluator = self.evaluator, question__isnull = False, assesment = False)  
        
    def get_stdoil(self):        
        try:
            data = StdOils.objects.get(select_oil__key = self.evaluator.stdoil_key)
        except Exception as e:           
            data = None            
        return data
    
    def get_nonanswered_questions(self):
        answered_question = set()
        for els in self.eva_label_statement:
            answered_question.add(els.question.id)            
        non_answered = [question.id for question in self.active_questions if question.id not in list(answered_question)]
        return non_answered
    
    def get_stdoil_result(self):
        oil_result = OilComparision(self.get_stdoil(), self.get_nonanswered_questions())
        data = oil_result.picked_labels_dict()   
        # print('With non answered question________________')     
        # print(data)
       
        return data
        
        
    def total_active_questions(self):
        # self.get_stdoil_result()
        data = self.active_questions.count()
        return round(data, 2)
    
    def positive_answered(self):
        positive_of_answer = self.eva_label_statement.filter(positive = str(1), dont_know = False)        
        unique_positive_question_ids = set()
        for poa in positive_of_answer:
            unique_positive_question_ids.add(poa.question.id)            
        return list(unique_positive_question_ids)       
        
    
    def total_positive_answer(self):
        # data = self.eva_label_statement.filter(positive = str(1)).values('question').distinct().count()      
        
        # return round(data, 2)
        return round(len(self.positive_answered()), 2)
    
    def negative_answered(self):
        negative_of_answer = self.eva_label_statement.filter(positive = str(0), dont_know = False)        
        unique_negative_question_ids = set()
        for poa in negative_of_answer:
            unique_negative_question_ids.add(poa.question.id)            
        return list(unique_negative_question_ids)  
        
    
    def total_nagetive_answer(self):
        # data = self.eva_label_statement.filter(positive = str(0)).values('question').distinct().count()
        # return round(data, 2)
        return round(len(self.negative_answered()), 2)
        
    
    def overview_green(self):
        data = (self.total_positive_answer()/self.total_active_questions())*100
        return round(data, 2)
    
    def overview_red(self):
        data = (self.total_nagetive_answer()/self.total_active_questions())*100
        return round(data, 2)
    
    def overview_grey(self):
        # '''
        # As overview green and overview red is in parcent so we will deduct from 100 the both to equalized dividation in barchart.
        # As each question have no label and have multiple positive value or negative value so sum of labelwise questions result is diferent then actual total question.
        # For this reason to get rid of the mismatched result we had to deduct from 100 to get matching report in the barchart.        
        # '''
        # data = 100 - (self.overview_green() + self.overview_red())    
        # return round(data, 2)
        negative_and_positive = self.positive_answered() + self.negative_answered()
        not_answered_or_donot_know = [question.id for question in self.active_questions if question.id not in negative_and_positive]
        
        return round(len(not_answered_or_donot_know), 2)
    
    def total_result(self):
        '''
        As per writen CSS our fist stacked bar will be green, second bar will be grey and third bar will be red so 
        we will placed the value in the list acordingly. We need to decide label name here so that it will be easy to impleted along with labels as each label has predifiened name.
        '''
        #green>>grey>>red
        serialized_record = [self.overview_green(), self.overview_grey(), self.overview_red()]
        # if self.get_stdoil() is not None:
        #     serialized_record[1:2] = [((i*self.overview_grey())/100) for i in self.get_stdoil_result().get('Overview')]
        # print(serialized_record)    
        record = {
            
            'Overview' : serialized_record
            }
        # else:
        #     record = self.get_stdoil_result().get('Overview')
        # print('record____________________________')
        # print(record)
        return record
    
    def label_wise_positive_answered(self, label):  
        evalebel = label.labels.all()         
        data = self.eva_label_statement.filter(evalebel__in = evalebel, positive = str(1), dont_know = False).count()
        return round(data, 2)
    
    def label_wise_nagetive_answered(self, label): 
        evalebel = label.labels.all()    
        data = self.eva_label_statement.filter(evalebel__in = evalebel, positive = str(0), dont_know = False).count()
        return round(data, 2)
    
    def label_wise_result(self):       
        labels = DifinedLabel.objects.filter(common_status = False)
        record_dict = {}
        for label in labels:             
            positive = round(self.active_questions.filter(questions__name = label, questions__value = str(1)).count(), 2)  
            #As labelwise record is more then total question due to multi label selected for each question
            #so we will make it based on the total positive    
            positive_answered = round((self.label_wise_positive_answered(label)/self.active_questions.count())*positive, 2)       
            negative = round(self.active_questions.filter(questions__name = label, questions__value = str(0)).count(), 2)
            #same as positive
            negative_answered = round((self.label_wise_nagetive_answered(label)/self.active_questions.count())*negative, 2)     
            
            
            
            
            # positive = round(self.active_questions.filter(questions__name = label, questions__value = 1).count(), 2)
            # positive_answered = self.label_wise_positive_answered(label)
            # negative = round(self.active_questions.filter(questions__name = label, questions__value = 0).count(), 2)
            # negative_answered = self.label_wise_nagetive_answered(label)
            
            
            
            
            
            green = round((positive_answered/positive)*100, 2)
            red = round((negative_answered/negative)*100, 2)        
            
            serialized_record = [green , round(100-(green+red),2), red]
            # if self.get_stdoil() is not None:
            #     serialized_record[1:2] = [((i*round(100-(green+red),2))/100) for i in self.get_stdoil_result().get(label.name)]
            
            
            record = {
                #Same as total total result
                #green>>grey>>red
                label.name : serialized_record
            }        
            record_dict.update(record)         
        return record_dict
    
    def picked_labels_dict(self):
        label_result = {}    
        label_result.update(self.label_wise_result())
        label_result.update(self.total_result()) 
        return label_result
    
    def packed_labels(self):
        
        '''
        From dataframe we will take rows to use in JS's series.
        '''
        df = pd.DataFrame(self.picked_labels_dict())   
        return df
    
    def label_data_history(self):
        data = LabelDataHistory.objects.filter(evaluator = self.evaluator) 
        result_dict=[]
        for d in data:
            item_dict = {
                (d.created).strftime('%d-%m-%Y') : eval(d.items)
                }
            result_dict.append(item_dict)
        date_wise_df_list = []
        for rd in result_dict:
            for key, values in rd.items():
                vf = pd.DataFrame(values)
                vf_label = vf.columns.values.tolist()
                vf_data = vf.values.tolist()
                date_wise_df = {
                    key : [vf_label, vf_data]
                }
                date_wise_df_list.append(date_wise_df)       
        
        return date_wise_df_list
    
def nreport_context(request, slug): 
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
    
    label_data = LabelWiseData(get_report)
    
    df = label_data.packed_labels() 
    dfh = label_data.label_data_history()    
    
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
            setattr(na, 'is_active', 'Unknown for this report')     
        
            
        # we will take which is not completed    
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
        'site_name': get_current_site(request).name,
        'item_label' : df.columns.values.tolist(),
        'item_seris' : df.values.tolist(),
        'na_ac' : na_ac,
        'dfh' : dfh
    }

    return context
        


