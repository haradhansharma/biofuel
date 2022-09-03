from .models import *
from django.utils import timezone
from django_cron import CronJobBase, Schedule
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
    log.info(f"Collected active session's evaluator id set, which is {s_evs}")
    return list(s_evs)

def clear_evaluator():
    '''
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
            
    log.info(f'{total_deleted} incomplete report has been deleted!')
    return total_deleted

# crontab codein linux
# */5 * * * * source /home/ubuntu/.bashrc && source /home/ubuntu/env/bin/activate && python /home/ubuntu/project-root/manage.py runcrons > /home/ubuntu/project-root/cronjob.log   
class DeleteIncompleteReports(CronJobBase):
    log.info('Initializing CRONJOB to delete incomplete report!!')
    RUN_EVERY_MINS = 60
    RETRY_AFTER_FAILURE_MINS = 5
    MIN_NUM_FAILURES = 2    
    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'evaluation.delete_incomplete_reports'   
    
    def do(self):    
        clear_evaluator()
    


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


