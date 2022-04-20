from .models import *
from django.utils import timezone

#This function call each time during access the site by middlewear.
#This is a westage cleaning
#It happens after each hrs
#It is extra layer to avoid error in userpage and evaluation thank you page.
def clear_evaluator(request):
    evaluator = Evaluator.objects.all()
    try:
        for e in evaluator:
            if e.evaluation_set.count() == 0:
                EvaLabel.objects.filter(evaluator = e,  create_date__gte = timezone.now() + timezone.timedelta(hours=1)).delete()
                EvaComments.objects.filter(evaluator = e).delete()
                Evaluator.objects.get(id = e.id, create_date__gte = timezone.now() + timezone.timedelta(hours=1)).delete()
    except Exception as e:
        pass   
    


def get_current_evaluator(request):
    evaluator = Evaluator.objects.get(id = request.session['evaluator'])
    return evaluator

#calculated statement genarator for report, is called in evaluatin procedure. function name telling what is being calulated
def label_assesment_for_donot_know(request, evalebel):
    'label wise Sumamry'
    ans_to_the_label = EvaLebelStatement.objects.filter(evalebel = evalebel, evaluator = get_current_evaluator(request), question__isnull = False, assesment = False).values('evalebel').distinct().count()
    dont_know_ans_to_the_lebel = EvaLebelStatement.objects.filter(evalebel = evalebel, evaluator = get_current_evaluator(request), question__isnull = False, dont_know = 1, assesment = False).values('evalebel').distinct().count()
    dont_know_percent_to_the_label = (int(dont_know_ans_to_the_lebel) * 100)/int(ans_to_the_label)
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
def label_assesment_for_positive(request, evalebel):
    'label wise Sumamry'
    ans_to_the_label = EvaLebelStatement.objects.filter(evalebel = evalebel, evaluator = get_current_evaluator(request), question__isnull = False, assesment = False).values('evalebel').distinct().count()
    pos_ans_to_the_lebel = EvaLebelStatement.objects.filter(evalebel = evalebel, evaluator = get_current_evaluator(request), question__isnull = False, positive = 1, assesment = False).values('evalebel').distinct().count()
    positive_percent_to_the_label = (int(pos_ans_to_the_lebel) * 100)/int(ans_to_the_label)
    if positive_percent_to_the_label < 50:
        statement = 'Based on the response to the enquiry, the ' + str(evalebel.label.name).lower() + ' evaluation of your oil contains multiple serious shortcomings.'
    elif positive_percent_to_the_label < 75:
        statement = 'According to the response to the query, the ' + str(evalebel.label.name).lower() + ' evaluation of your oil is generally good. However, there are a few shortcomings that needs be addressed further.'
    elif positive_percent_to_the_label < 90:
        statement = 'According to the response to the inquery, the ' + str(evalebel.label.name).lower() + ' evaluation of your oil is largely favourable Nonetheless, the aformentioned issues must be considered in to account.'
    else:
        statement = 'According to the response to the query, the ' + str(evalebel.label.name).lower() + ' evaluation of your oil is highly promising. It has a lot of promise in terms of the ' + str(evalebel.label.adj).lower() + '.'

    return statement

#calculated statement genarator for report, is called in evaluatin procedure. function name telling what is being calulated
def overall_assesment_for_donot_know(request, evalebel):
    ans_ques = EvaLebelStatement.objects.filter(evaluator = get_current_evaluator(request), question__isnull = False, assesment = False).values('question').distinct().count()
    dont_know_ans = EvaLebelStatement.objects.filter(evaluator = get_current_evaluator(request), question__isnull = False, dont_know = 1, assesment = False).values('question').distinct().count()
    dont_know_percent = (int(dont_know_ans) * 100)/int(ans_ques)

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
def overall_assesment_for_positive(request, evalebel):
    ans_ques = EvaLebelStatement.objects.filter(evaluator = get_current_evaluator(request), question__isnull = False, assesment = False).values('question').distinct().count()
    pos_ans = EvaLebelStatement.objects.filter(evaluator = get_current_evaluator(request), question__isnull = False, positive = 1, assesment = False).values('question').distinct().count()
    positive_percent = (int(pos_ans) * 100)/int(ans_ques)
    if positive_percent < 50:
        statement = 'Based on the response to the enquiry, the ' + 'overall' + ' evaluation of your oil contains multiple serious shortcomings.'
    elif positive_percent < 75:
        statement = 'According to the response to the query, the ' + 'overall' + ' evaluation of your oil is generally good. However, there are a few shortcomings that needs be addressed further.'
    elif positive_percent < 90:
        statement = 'According to the response to the inquery, the ' + 'overall' + ' evaluation of your oil is largely favourable Nonetheless, the aformentioned issues must be consdered in to account.'
    else:
        statement = 'According to the response to the query, the ' + 'overall' + ' evaluation of your oil is highly promising. It has a lot of promise in terms of the ' + str(evalebel.label.adj).lower() + '.'

    return statement


