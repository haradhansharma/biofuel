from django.utils import timezone
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from evaluation.models import *
from accounts.models import *
from django.db.models import Count, Min
from django.db.models.functions import TruncDay
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
log =  logging.getLogger('log')
def total_reports(request):
    total_reports = Evaluator.objects.all().count()
    return total_reports
def total_this_user_report(request):
    total_reports = Evaluator.objects.filter(creator = request.user).count()
    return total_reports

def users_under_each_label(request):    
    labels = DifinedLabel.objects.filter(common_status = False)
    record_dict = {}
    for label in labels:       
        record = {
            label.name : User.objects.filter(experts_in = label, is_active = True).count()
        }
        record_dict.update(record)   
    
    return record_dict

def reports_under_each_biofuel(request):    
    biofuels = Biofuel.objects.all()
    record_dict = {}
    for biofuel in biofuels:       
        record = {
            biofuel.name : Evaluator.objects.filter(biofuel = biofuel).count()
        }
        record_dict.update(record)   
    
    return record_dict

def weeks_results(request):
    # first_date_of_report = (Evaluator.objects.all().order_by('create_date').first()).create_date
    day_last_week = (timezone.now() - timezone.timedelta(days=365))    
 
    reports = Evaluator.objects.filter(create_date__gte=day_last_week).values('create_date__date').annotate(total = Count('create_date__date'))   
    records = {}
    for i in reports:
        record = {
           i['create_date__date'].strftime("%m/%y") : i['total']
        }
        records.update(record)     
  
    return records

def all_reports(request):
    try:
        if request.user.is_staff or request.user.is_superuser:
            reports = Evaluator.objects.filter(report_genarated = True).order_by('-create_date')  
        else:
            reports = Evaluator.objects.filter(creator = request.user , report_genarated = True).order_by('-create_date')  
    
        if reports.exists():
            reports_set = [] 
            for evaluator in reports:
                answered_questiones = EvaLebelStatement.objects.filter(evaluator = evaluator).exclude(question = None).values('question').distinct().count()
                positive_ans = EvaLebelStatement.objects.filter(evaluator = evaluator, positive=str(1)).exclude(question = None).values('question').distinct().annotate(positive = Count('positive')).count()
                dont_know_ans = EvaLebelStatement.objects.filter(evaluator = evaluator, dont_know=True).exclude(question = None).values('question').distinct().annotate(positive = Count('dont_know')).count() 
                dont_know_percent = (int(dont_know_ans) * 100)/int(answered_questiones) if answered_questiones != 0 else 100
                positive_percent = (int(positive_ans) * 100)/int(answered_questiones) if answered_questiones != 0 else 100     
                
                g_report = {
                    'report': evaluator,
                }  
                g_report_result = {
                    'answered_questiones' : answered_questiones,
                    'positive_ans' : positive_ans,
                    'dont_know_ans' : dont_know_ans,
                    'dont_know_percent': str("%.2f" % dont_know_percent) + '%', 
                    'positive_percent': str("%.2f" % positive_percent) + '%',  
                }  
                
                robj = {
                    'g_report': g_report,
                    'g_report_result': g_report_result,           
                }
            
                reports_set.append(robj)
            
            page = request.GET.get('page', 1)
            paginator = Paginator(reports_set, 10)
            try:
                reports_set = paginator.page(page)
            except PageNotAnInteger:
                reports_set = paginator.page(1)
            except EmptyPage:
                reports_set = paginator.page(paginator.num_pages)   
            
            return reports_set
        else:
            return None    
    except Exception as e:
        log.warning(f'All report abroted due to {e}')    
        raise Http404

def typewise_user(request):    
    user_types = UserType.objects.all()
    record_dict = {}
    for user_type in user_types:       
        record = {
            user_type : User.objects.filter(usertype = user_type)[:4]
        }
        record_dict.update(record)   
    
    return record_dict


        
    
    