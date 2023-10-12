from django.utils import timezone
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from evaluation.models import *
from accounts.models import *
from django.db.models import Count, Min, Sum, Case, When, IntegerField, F, Prefetch
from django.db.models.functions import TruncDay
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from evaluation.helper import get_biofuel, get_all_definedlabel

import logging
log =  logging.getLogger('log')

# Method to calculate the total number of reports in the database.
def total_reports(request):
    """
    Calculate the total number of reports in the database.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        int: The total number of reports.
    """
    total_reports = Evaluator.objects.all().count()
    return total_reports

# Method to calculate the total number of reports created by the current user.
def total_this_user_report(request):
    """
    Calculate the total number of reports created by the current user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        int: The total number of reports created by the current user.
    """
    total_reports = Evaluator.objects.filter(creator = request.user).count()
    return total_reports

# Method to count the number of users under each label.
def users_under_each_label(request):   
    """
    Count the number of users under each label.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary where keys are label names and values are the count of users under each label.
    """ 
    labels = get_all_definedlabel().filter(common_status = False)    
    
    # Prefetch related users for each label to optimize database queries.
    prefetch = Prefetch('user_label', queryset=User.objects.filter(is_active=True), to_attr='active_users')
    labels = labels.prefetch_related(prefetch)    
    
    record_dict = {}
    for label in labels:          
        count = len(getattr(label, 'active_users', []))
        record_dict[label.name] = count
    
    return record_dict

# Method to count the number of reports under each biofuel category.
def reports_under_each_biofuel(request):    
    """
    Count the number of reports under each biofuel category.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary where keys are biofuel names and values are the count of reports under each biofuel category.
    """
    biofuels = get_biofuel()
    record_dict = {}
    for biofuel in biofuels:
        record_dict[biofuel.name] = len(biofuel.eva_fuel.all())
    return record_dict


# Method to retrieve the number of reports generated in the last year.
def weeks_results(request):
    """
    Retrieve the number of reports generated in the last year and format the results.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary where keys are formatted date strings (month/year) and values are report counts.
    """
    # Calculate the date one year ago from the current date.
    
    # first_date_of_report = (Evaluator.objects.all().order_by('create_date').first()).create_date
    day_last_week = (timezone.now() - timezone.timedelta(days=365))    
    
    # Query the database to count reports created in the last year.
    reports = Evaluator.objects.filter(create_date__gte=day_last_week).values('create_date__date').annotate(total = Count('create_date__date'))   
    
    records = {}
    for i in reports:
        record = {
           i['create_date__date'].strftime("%m/%y") : i['total']
        }
        records.update(record)     
  
    return records

# Method to retrieve and filter reports based on user roles.
def all_reports(request):
    """
    Retrieve and filter reports based on user roles and calculate additional statistics.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Paginator: A paginated list of reports along with additional statistics.
    """
    try:  
        # Check if the user is a staff member or superuser to show all reports.         
        if request.user.is_staff or request.user.is_superuser:
            reports = Evaluator.objects.select_related('biofuel').filter(report_genarated=True).order_by('-create_date')
        else:
            reports = Evaluator.objects.select_related('biofuel').filter(creator=request.user, report_genarated=True).order_by('-create_date')
        
    
        if reports.exists():
            reports_set = []             
            
             # Count the number of answered, positive, and don't know responses for each report.
            question_counts = EvaLebelStatement.objects.filter(evaluator__in=reports).exclude(question=None).values('evaluator').annotate(count=Count('question', distinct=True)).values('evaluator', 'count')
            positive_counts = EvaLebelStatement.objects.filter(evaluator__in=reports, positive='1').exclude(question=None).values('evaluator').annotate(count=Count('question', distinct=True)).values('evaluator', 'count')
            dont_know_counts = EvaLebelStatement.objects.filter(evaluator__in=reports, dont_know=True).exclude(question=None).values('evaluator').annotate(count=Count('question', distinct=True)).values('evaluator', 'count')
            
            
            question_counts_dict = {item['evaluator']: item['count'] for item in question_counts }
            positive_counts_dict = {item['evaluator']: item['count'] for item in positive_counts}
            dont_know_counts_dict = {item['evaluator']: item['count'] for item in dont_know_counts}
            
            
            for evaluator in reports:                
                
                answered_questiones = question_counts_dict.get(evaluator.pk, 0)
                positive_ans = positive_counts_dict.get(evaluator.pk, 0)
                dont_know_ans = dont_know_counts_dict.get(evaluator.pk, 0)
                dont_know_percent = (dont_know_ans * 100) / answered_questiones if answered_questiones != 0 else 100
                positive_percent = (positive_ans * 100) / answered_questiones if answered_questiones != 0 else 100    
                
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
            
            # Paginate the results with 10 reports per page.
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
    """
    Retrieve user types and their associated users.

    This function fetches all user types and prefetches related users for each user type. 
    It returns a dictionary where keys are user type objects and values are lists of associated users, limited to the first 4 users for each type.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: A dictionary where keys are user type objects and values are lists of associated users.
    """
    user_types = UserType.objects.all().prefetch_related('user_usertype')
    record_dict = {}
    for user_type in user_types:    
        # Limit the list of associated users to the first 4 for each user type.   
        record_dict[user_type] = user_type.user_usertype.all()[:4]
    
    return record_dict

        
    
    