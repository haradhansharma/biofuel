import uuid
from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify
import random
import string


#Validator in admin to protect from more then one common status to be entry.
def get_common_status(value):
    try:
        common_status_total = DifinedLabel.objects.filter(common_status = True).count()
        common_status = DifinedLabel.objects.get(common_status = True)
    except Exception:
        common_status_total = 0

    if common_status_total == int(1) and value == 1:
        raise ValidationError('A common status named "' + common_status.name +'" already exist! Only One common status allowed!')
    else:
        pass
    
    



class DifinedLabel(models.Model):
    '''
    # database connector for label to use in sidewide
    # We need to define labe to work in report and each question settings in admin.
    
    ''' 
    
    
    name = models.CharField(max_length=252) 
    
    # label to be display on the evaluation's question form
    label = models.CharField(max_length=252, default='')
    
    #adj to use alternative name in the statement
    adj = models.CharField(max_length=252, default='')
    
    # Summary should be marked as common_status
    common_status = models.BooleanField(default=False, validators=[get_common_status])
    
    #sor_order is most importent to maintain display order
    sort_order = models.CharField(max_length=3, default=0)

    def __str__(self):
        return self.name

   
def generate_uuid():
    '''
    # genarate hexacode for slug url. currently it is beeing used only on questions.
    '''
    return uuid.uuid4().hex





class Question(models.Model):
    '''
    # database connection for questions
    # IF question is parent then have to be selected is_door
    # Active question is accessible everywhere, if please keep careful eye to tick mark on is_active.
    # To make question chaptaries have to select parent_question
    # sort_order is most important to work system corrctly. So be careful here.
    # do not touch the slug.
    # parent question must be mark by giving tick mark on is_door with proper short_order.
    # every question should have proper sort order and must be selected next_question in option part(mentioned below) to go to next question otherwise system will redirect to the that you page of report.
    '''
    slug = models.CharField(default=generate_uuid, editable=False, unique=True, max_length=40)
    name = models.CharField(max_length=252)
    chapter_name = models.CharField(max_length=252, null=True, blank=True)
    parent_question = models.ForeignKey("evaluation.Question", on_delete=models.CASCADE, null=True, blank=True, related_name='child' )
    sort_order = models.IntegerField(default=1)    
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    is_door = models.BooleanField(default=False)
    chart_title = models.CharField(max_length=252, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return  '(' + str(self.sort_order) +') ' + self.name
    
    #The url to brows indivisual question to edit but it is not usefule in evaluation procedure.
    def get_absolute_url(self):        
        return reverse('home:questions_details', args=[str(self.slug)])
    
    
    # the url to add quatation to the questions 
    @property
    def add_quatation(self):
        return reverse('home:add_quatation', args=[str(self.slug)])
    
    
    @property
    def labels(self):
        return Label.objects.filter(question = self)
    
    @property
    def get_related_quotations(self):   
        from home.models import Quotation
        quotations = Quotation.objects.filter(related_questions = self)        
        return quotations
    
    @property
    def get_quotations(self):         
        from home.models import Quotation
        quotations = Quotation.objects.filter(test_for = self)        
        return quotations
    
    @property
    def get_options(self):
        return self.question.all()
    
    @property
    def get_stdoils(self):
        return self.stanchart.all()
    
    @property
    def have_4labels(self):
        labels = self.questions.filter(value = '1').count()
        if labels > 0:
            return True
        return False
    
    @property
    def problem_in_option(self):
        options = self.question.all()
        
        total_option = options.count()
        if total_option >= 3 :
            option_ok = True
        else:
            option_ok = False
            
        status_marking = [o for o in options if (o.yes_status and o.positive == '0') or (o.dont_know and o.positive == '1') or (o.name.lower() == 'no' and o.positive == '1')]
        if len(status_marking) > 0:
            status_ok = True
        else:
            status_ok = False
            
        if option_ok and status_ok:
            return False        
        return True
            
        
    
 
class Label(models.Model):
    '''
    # database conenctor for labels
    # The label has to be set during seting up questions.
    # so that this is made inline in the admin side.
    # Value is the formulated field as per business logic.
    '''
    name = models.ForeignKey(DifinedLabel, on_delete=models.PROTECT, related_name='dlabels', limit_choices_to={'common_status': False})
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='questions')
    value = models.CharField(max_length=1, default=0)
    
    

    def __str__(self):
        return self.name.name

class Option(models.Model):  
    '''
    # database conenctor for options
    # if name is 'Yes' or not but option represent yes then 'yes_status' must be marked, otherwise system will give wrong result and behave unexected.
    # if name is 'Don't Know' or not but represent do not know then 'dont_know' must be tick marked, otherwise system will give wrong result and behave unexected.
    # if name 'No' or not but represent as 'no' then 'name' should be writen as 'No'(Case sensative), otherwise system will give wrong result and behave unexected.
    # 'next_question' must be selected to go to the next question during process of evaluation otherwise system will redirect to the thank you page.
    # 'statement' will be printed under label in report and question page based on selection of questions.
    # 'next_step' will be printed under the label based on selection as per business logic in report and question forms.
    # 'overall' should be filled as 1 or 0 (It was recomended during development, and advised to avoid True/Flse). if overall is 1 then statement will be added to the summary.
    # 'positive' should be filled as 1 or 0 (It was recomended during development, and advised to avoid True/Flse). it is used to calculated assesent under the label in report and question form.
    # When updated any statement or next_step evaluator notify status will be updated by signal 'on_change'
    '''  
    name = models.CharField(max_length=252)
    yes_status = models.BooleanField(default=False)
    dont_know = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')
    next_question = models.ForeignKey(Question, on_delete=models.CASCADE, null = True, blank = True, related_name='next_question', limit_choices_to={'is_active': True})
    statement = models.TextField(null = True, blank = True,)
    next_step = models.TextField(null = True, blank = True,)
    overall = models.CharField(max_length=1, default=0)
    positive = models.CharField(max_length=1, default=0)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)
    

    def __str__(self):
        return self.name + '(' + str(self.question.sort_order) + ')'

class LogicalString(models.Model):
    '''
    # database conenctor for logical statement based on selected options.
    # As per business logic it is another part of statement.
    # can selecte multi option. 
    # 'tex' is act as statment.
    # based on selection statement will be added to the labels of report and questions form
    # 'overall' should be filled as 1 or 0 (It was recomended during development, and advised to avoid True/Flse). if overall is 1 then statement will be added to the summary.
    # 'positive' should be filled as 1 or 0 (It was recomended during development, and advised to avoid True/Flse). it is used to calculated assesent under the label in report and question form.
    '''
    options = models.ManyToManyField(Option)
    text = models.TextField(null = True, blank = True,)
    overall = models.CharField(max_length=1, default=0)
    positive = models.CharField(max_length=1, default=0)
        
    @property
    def option_list(self):
        option_set = [str(option.id) for option in self.options.all()]       
        return str(sorted(option_set))
    
    @property
    def Label_value_one_to(self):
        assigned = [label.name for label in self.logical_strings.filter(value=1) ]
        return assigned
            

    def __str__(self):
        #do not change this, if done then return same as optionset
        return self.text
    
    
        
    
class OptionSet(models.Model):
    '''    
    It has been genarated autometically during evaluation by user.
    so that it is not displayed in admin side.    
    '''
    option_list = models.CharField(max_length=252, unique = True)
    text = models.TextField()
    positive = models.CharField(max_length=1, default=0)
    overall = models.CharField(max_length=1, default=0)
    ls_id = models.CharField(max_length=252, default=0)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)


    def __str__(self):
        #do not change below, if done then return same as logicalstring
        return self.text

class Lslabel(models.Model):
    '''
    # Labels for logical string to select during seting up logical string
    # It is mandatory.    
    '''
    
    name = models.ForeignKey(DifinedLabel, on_delete=models.PROTECT, related_name='ls_dlabels', limit_choices_to={'common_status': False})
    logical_string = models.ForeignKey(LogicalString, on_delete=models.CASCADE, related_name='logical_strings')
    value = models.CharField(max_length=1, default=0)

    def __str__(self):
        return self.name.name

class Biofuel(models.Model):
    '''
    The biofuel selected by user in initial page of evaluation.
    Based on this value a summary has been displayed under the dashboard.    
    '''
    name = models.CharField(max_length=252)
    
    
    def __str__(self):
        return self.name
    

    

class Evaluator(models.Model):
    # from . models import StandaredChart
    '''
    Do not edit or modyfy anything here from admin side.
    It has been genarated autometically during evaluation by user.
    so that it is not editable in admin side.
    
    '''
    slug = models.UUIDField( default=uuid.uuid4, editable=False, unique=True)    
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user')    
    name = models.CharField(max_length=252)
    email = models.EmailField()
    phone = models.CharField(max_length=16, null=True, blank=True)
    orgonization = models.CharField(max_length=252, null=True, blank=True)
    biofuel = models.ForeignKey(Biofuel, on_delete=models.SET_NULL, null=True, blank=True)
    stdoil_key = models.CharField(max_length=20, null=True, blank=True)
    
   
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)
    report_genarated = models.BooleanField(default=False)
    
    # it is been updated when statement and next_step of option has been changed and when genarate new report based on report 
    feedback_updated = models.BooleanField(default=False)
    
    
        
    
    
    #Colored output of Pending to notify to the evaluator about feedback update of option
    def notified(self):
        if self.feedback_updated:
            return mark_safe('<b style="background:{};padding:5px;color:#ffffff;" >{}</b>'.format('green', self.feedback_updated))
        else:
            return mark_safe('<b style="background:{};padding:5px;color:#ffffff;" >{}</b>'.format('orange', 'Pending'))
    

    def __str__(self):
        return self.name + str(self.id)
    
    def get_absolute_url(self):
        return reverse('evaluation:nreport', args=[str(self.slug)])    


class Evaluation(models.Model):
    '''    
    It has been genarated autometically during evaluation by user.
    so that it is not displayed in admin side.    
    '''
    evaluator = models.ForeignKey(Evaluator, on_delete=models.RESTRICT, related_name='eva_evaluator')
    option = models.ForeignKey(Option, on_delete=models.RESTRICT, related_name='eva_option')
    question = models.ForeignKey(Question, on_delete=models.RESTRICT,null=True, blank=True, related_name='eva_question')
    

    def __str__(self):
        return self.evaluator.name

    @property
    def get_question_comment(self):
        eva_comment = EvaComments.objects.filter(question = self.question, evaluator = self.evaluator)
        return eva_comment


class EvaComments(models.Model):
    '''    
    It has been genarated autometically during evaluation by user.
    so that it is not displayed in admin side.    
    '''
    evaluator = models.ForeignKey(Evaluator, on_delete=models.RESTRICT, related_name='coment_evaluator')
    question = models.ForeignKey(Question, on_delete=models.RESTRICT, related_name='comment_question')
    comments = models.TextField(max_length=600)

    def __str__(self):
        return self.comments


class EvaLabel(models.Model):
    '''    
    It has been genarated autometically during evaluation by user.
    so that it is not displayed in admin side.    
    '''
    label = models.ForeignKey(DifinedLabel, on_delete=models.PROTECT, related_name='labels')
    evaluator = models.ForeignKey(Evaluator, on_delete=models.RESTRICT, related_name='evaluators')
    sort_order = models.CharField(max_length=3, default=0)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.label.name

class EvaLebelStatement(models.Model):
    '''    
    It has been genarated autometically during evaluation by user.
    so that it is not displayed in admin side.    
    '''
    evalebel = models.ForeignKey(EvaLabel, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT, null=True, blank=True)
    option_id = models.CharField(max_length=252, null=True, blank=True)
    statement = models.TextField(blank=True, null=True)
    next_step = models.TextField(blank=True, null=True)
    positive = models.CharField(max_length=1, default=0)
    dont_know = models.BooleanField(default=False)
    assesment = models.BooleanField(default=False)
    next_activity = models.BooleanField(default=False)
    evaluator = models.ForeignKey(Evaluator, on_delete=models.RESTRICT, related_name='s_evaluators', null=True)    
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)

    def __str__(self):
        return self.statement
    @property
    def is_positive(self):
        if self.positive == str(1):
            return True
        return False
    @property
    def is_negative(self):
        if self.positive == str(0) and self.dont_know == False:
            return True
        return False
    
    @property
    def is_dontknow(self):
        if self.dont_know == True:
            return True
        return False
    

    
    
class NextActivities(models.Model):
    '''
    Main parameter to be set here for next activities.
    '''
    name_and_standared = models.CharField(max_length=250)
    short_description = models.TextField(max_length=152)
    descriptions = models.TextField()
    url = models.URLField(null=True, blank=True)
    priority = models.CharField(max_length=2)
    related_questions = models.ManyToManyField(Question, related_name="related_next", verbose_name="Please select related questions", help_text="Allow multiple option selection. The selected options should be highlighted.", limit_choices_to={'is_active': True})
    compulsory_questions = models.ManyToManyField(Question, related_name="compulsory_next", verbose_name="Please select compulsory questions", help_text="Allow multiple. The selected options should be highlighted.", limit_choices_to={'is_active': True})
    related_percent = models.IntegerField()
    compulsory_percent = models.IntegerField()    
    is_active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)
    
    
    def __str__(self):
        return str(self.name_and_standared)
    
    def get_quotations(self):
        quotations = set()
        for question in self.related_questions.all():
            for quotation in question.get_quotations:
                quotations.add(quotation)
            for quotation in question.get_related_quotations:
                quotations.add(quotation)
        return quotations
                
    

class EvaluatorActivities(models.Model):
    '''    
    It has been genarated autometically during evaluation by user.
    so that it is not displayed in admin side.    
    '''
    evaluator = models.ForeignKey(Evaluator, on_delete=models.CASCADE, related_name="eaevaluator")    
    next_activity = models.ForeignKey(NextActivities, on_delete=models.CASCADE, related_name="eanextactivities")
    related_percent = models.IntegerField()
    compulsory_percent = models.IntegerField()
    is_active = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)
    
    def __str__(self):
        return str(self.next_activity.name_and_standared)
    
class OliList(models.Model):
    name = models.CharField(max_length = 250, unique=True)
    key = models.CharField(null=True, blank=True, editable=False, max_length=250)    
    
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):  
        key_sample = slugify(self.name)    
        self.key = key_sample
        super(OliList, self).save(*args, **kwargs)
    
    
    
    
    
class StdOils(models.Model):    
    select_oil = models.ForeignKey(OliList, on_delete=models.CASCADE, default=1)
    biofuel = models.ForeignKey(Biofuel, on_delete=models.SET_NULL, null=True, editable=False,)
    
    
    def __str__(self):
        return self.select_oil.name

class StandaredChart(models.Model):
    '''
    Please check admin for this model if you changing anythig as here option is overwriting form admin to narrow down.
    '''
    from home.models import WeightUnit      
    from smart_selects.db_fields import ChainedForeignKey
    oil = models.ForeignKey(StdOils, on_delete=models.CASCADE,  related_name = 'std_oil_of_chart',)    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="stanchart", limit_choices_to={'is_active': True})
    unit = models.ForeignKey(WeightUnit, on_delete=models.CASCADE, related_name= "chrartunit", null=True, blank=True)
    value = models.CharField(max_length=252, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    # option = models.ForeignKey(Option, on_delete=models.SET_NULL, related_name='stoption', null=True, blank=True)
    option = ChainedForeignKey(Option, chained_field="question", chained_model_field="question", show_all=False,auto_choose=True, sort=True, on_delete=models.SET_NULL, related_name='stoption', null=True, blank=True)
    
    
    @property
    def oil_key(self):
        return self.oil.selected_oil.key.lower() 
    
    
    
        
    def __str__(self):
        return self.oil.select_oil.name
    
    
#to reduce youtube API call we will save the dat in our databse
class Youtube_data(models.Model):
    term = models.TextField()
    urls = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.term
    
class LabelDataHistory(models.Model):
    evaluator = models.ForeignKey(Evaluator, on_delete=models.CASCADE)
    # label = models.TextField(max_length=250)
    items= models.TextField(max_length=250)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.items
    
    
#The mail ques will be executed by crontab and will e created during saving BlogPost   
class ReportMailQueue(models.Model):
    to = models.CharField(max_length=256, null=True, blank=True)
    from_report = models.ForeignKey(Evaluator, on_delete=models.CASCADE, related_name='reportquefrom')   
    new_report = models.ForeignKey(Evaluator, on_delete=models.CASCADE, related_name='reportqueto')         
    added_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    process_time = models.DateTimeField(auto_now=True)
    tried=models.IntegerField(default=0)
    
    def __str__(self):
        return self.to
    
    
