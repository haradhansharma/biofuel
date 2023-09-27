import uuid
from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify
import random
import string
from django.db.models import Count

# Validator in admin to protect from more than one common status entry.
def get_common_status(value):
    """
    Validate that there is only one common status entry in DifinedLabel objects.

    :param value: The value to check (usually 1 for common status).
    :raises ValidationError: Raised if there is already a common status defined.
    """
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
    """
    Database connector for labels used site-wide.
    Labels are used in reports and question settings in the admin.
    Common status can only be one.
    """
    
    class Meta:
        verbose_name = 'Defined Label'
        verbose_name_plural = 'Defined Labels'
    
    
    name = models.CharField(max_length=252)   
    label = models.CharField(max_length=252, default='')
    adj = models.CharField(max_length=252, default='')
    common_status = models.BooleanField(default=False, validators=[get_common_status])
    sort_order = models.CharField(max_length=3, default=0)

    def __str__(self):
        return self.name

   
def generate_uuid():
    """
    Generate a hexadecimal code for slug URL (currently used only on questions).
    """
    return uuid.uuid4().hex


class Question(models.Model):
    """
    Database connection for questions.
    - If a question is a parent, it must be selected as 'is_door'.
    - Active questions are accessible everywhere; use 'is_active' to control.
    - To make questions part of a chapter, select 'parent_question'.
    - 'sort_order' is crucial for correct system operation.
    - Do not modify the slug.
    - Parent questions must be marked as 'is_door' with proper 'sort_order'.
    - Every question should have a proper 'sort_order' and be linked to the 'next_question' in options.
      Otherwise, the system will redirect to the report page.
    """
    slug = models.CharField(default=generate_uuid, editable=False, unique=True, max_length=40, db_index=True)
    name = models.CharField(max_length=252)
    chapter_name = models.CharField(max_length=252, null=True, blank=True)
    parent_question = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name='child', db_index=True )
    sort_order = models.IntegerField(default=1)    
    description = models.TextField()
    is_active = models.BooleanField(default=False, db_index=True)
    is_door = models.BooleanField(default=False, db_index=True)
    chart_title = models.CharField(max_length=252, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)

    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        return  '(' + str(self.sort_order) +') ' + self.name
    
    
    def get_absolute_url(self):   
        """
        Get the URL to browse an individual question for editing (not used in the evaluation procedure).
        """     
        return reverse('home:questions_details', args=[str(self.slug)])
    
    
    
    @property
    def add_quatation(self):
        """
        Get the URL to add a quotation to the question.
        """
        return reverse('home:add_quatation', args=[str(self.slug)]) 
    
    
    @property
    def labels(self):
        """
        Get labels related to this question.
        """
        return Label.objects.filter(question = self)
    
    
    @property
    def get_related_quotations(self): 
        """
        Get related quotations for this question.
        
        """  
        quotations = self.quotations_related_questions.all()  
        return quotations
    
    @property
    def get_quotations(self): 
        """
        Get quotations associated with this question.        
        """       
        
        quotations = self.testfor.all()
                         
        return quotations
     
    
    @property
    def get_merged_quotations(self):
        """
        Get merged quotations, including related and associated quotations.
        """
        from itertools import chain             
        result_set = set(chain(self.get_related_quotations, self.get_quotations))     
        result_list =  list(result_set)     
        return result_list
        
    
    @property
    def get_options(self):
        """
        Get options for this question.
        """
        from evaluation.helper import get_options_of_ques
        return get_options_of_ques(self)
    
    @property
    def get_stdoils(self):
        """
        Get standard oils for this question.
        """
        return self.stanchart.all()
    
    
    def have_4labels(self):
        """
        Check if the question has at least 4 labels.
        """
        labels = self.questions.filter(value='1').annotate(label_count=Count('id')).values('label_count').first()
        if labels and labels['label_count'] > 0:
            return True
        return False
    
    @property
    def problem_in_option(self):
        """
        Check for problems in question options.
        """
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
    
    @property
    def not_is_door_nor_have_parent(self):     
        """
        Check if the question is neither a door nor has a parent.
        """   
        if self.is_door == False and not self.parent_question and self.is_active:
            return True
        return False
    
    @property
    def get_sugestions(self):
        """
        Get suggestions related to this question.
        """
        from evaluation.helper import get_sugestions_of_ques
        sugestions = get_sugestions_of_ques(self)
        return sugestions            
        
    
 
class Label(models.Model):
    '''
    Database connector for labels.
    Labels are set during the setup of questions.
    They are managed inline in the admin side.
    The 'value' field is formulated according to business logic.
    '''
    name = models.ForeignKey(DifinedLabel, on_delete=models.PROTECT, related_name='dlabels', limit_choices_to={'common_status': False})
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='questions', db_index=True)
    value = models.CharField(max_length=1, default=0)
    
    

    def __str__(self):
        return self.name.name

class Option(models.Model):  
    '''
    Database connector for options.
    - If the option represents 'Yes', 'yes_status' must be marked.
    - If the option represents 'Don't Know', 'dont_know' must be ticked.
    - If the option represents 'No', 'name' should be written as 'No' (case-sensitive).
    - 'next_question' must be selected to go to the next question during the evaluation process; otherwise, the system will redirect to the thank-you page.
    - 'statement' will be printed under the label in the report and question page based on question selection.
    - 'next_step' will be printed under the label based on business logic in report and question forms.
    - 'overall' should be filled as '1' or '0' (recommended to avoid True/False). If 'overall' is '1', the statement will be added to the summary.
    - 'positive' should be filled as '1' or '0' (recommended to avoid True/False). It is used to calculate assessment under the label in report and question form.
    - When updating any statement or next_step, the evaluator notify status will be updated by the 'on_change' signal.
    '''
    name = models.CharField(max_length=252)
    yes_status = models.BooleanField(default=False, db_index=True)
    dont_know = models.BooleanField(default=False, db_index=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question', db_index=True)
    next_question = models.ForeignKey(Question, on_delete=models.CASCADE, null = True, blank = True, related_name='next_question', limit_choices_to={'is_active': True}, db_index=True)
    statement = models.TextField(null = True, blank = True,)
    next_step = models.TextField(null = True, blank = True,)
    overall = models.CharField(max_length=1, default=0, db_index=True)
    positive = models.CharField(max_length=1, default=0, db_index=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)
    

    def __str__(self):
        return f"{self.name} ({self.question.sort_order})"

class LogicalString(models.Model):
    '''
    Database connector for logical statements based on selected options.
    This is another part of the statement according to business logic.
    Multiple options can be selected.
    'text' acts as the statement.
    Based on selection, the statement will be added to the labels of reports and question forms.
    'overall' should be filled as '1' or '0' (recommended to avoid True/False). If 'overall' is '1', the statement will be added to the summary.
    'positive' should be filled as '1' or '0' (recommended to avoid True/False). It is used to calculate assessment under the label in reports and question forms.
    '''
    options = models.ManyToManyField(Option, db_index=True)
    text = models.TextField(null = True, blank = True,)
    overall = models.CharField(max_length=1, default=0, db_index=True)
    positive = models.CharField(max_length=1, default=0, db_index=True)
        
    @property
    def option_list(self):
        option_set = [str(option.id) for option in self.options.all()]       
        return str(sorted(option_set))
    
    @property
    def Label_value_one_to(self):
        assigned = [label.name for label in self.logical_strings.filter(value = '1') ]
        return assigned
    
    @property
    def have_4labels(self):
        labels = self.logical_strings.filter(value = '1').count()
        if labels > 0:
            return True
        return False
            

    def __str__(self):
        # Do not change this; if done, then return the same as the option set
        return self.text   
    
       
    
class OptionSet(models.Model):
    '''    
    Automatically generated during evaluation by the user.
    Not displayed in the admin side.    
    '''
    option_list = models.CharField(max_length=252, unique = True, db_index=True)
    text = models.TextField()
    positive = models.CharField(max_length=1, default=0, db_index=True)
    overall = models.CharField(max_length=1, default=0, db_index=True)
    ls_id = models.CharField(max_length=252, default=0)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)


    def __str__(self):        
        # Do not change below; if done, then return the same as the logical string
        return self.text

class Lslabel(models.Model):
    '''
    Labels for logical strings to select during the setup of logical strings.
    Mandatory to select.
    '''
    
    name = models.ForeignKey(DifinedLabel, on_delete=models.PROTECT, related_name='ls_dlabels', limit_choices_to={'common_status': False})
    logical_string = models.ForeignKey(LogicalString, on_delete=models.CASCADE, related_name='logical_strings', db_index=True)
    value = models.CharField(max_length=1, default=0)

    def __str__(self):
        return self.name.name

class Biofuel(models.Model):
    '''
    The biofuel selected by the user on the initial page of evaluation.
    Based on this value, a summary is displayed under the dashboard.
    '''
    name = models.CharField(max_length=252)
    
    
    def __str__(self):
        return self.name
    

    

class Evaluator(models.Model):       
    '''
    Do not edit or modify anything here from the admin side.
    Automatically generated during evaluation by the user.
    Not editable in the admin side.
    '''
    slug = models.UUIDField( default=uuid.uuid4, editable=False, unique=True, db_index=True)    
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='user', db_index=True)    
    name = models.CharField(max_length=252)
    email = models.EmailField()
    phone = models.CharField(max_length=16, null=True, blank=True)
    orgonization = models.CharField(max_length=252, null=True, blank=True)
    biofuel = models.ForeignKey(Biofuel, on_delete=models.SET_NULL, null=True, blank=True, related_name='eva_fuel', db_index=True)
    stdoil_key = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    make_it_public = models.BooleanField(default=True, help_text="By default it is public! If not tick marked it will not be visible to the site!")
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)
    report_genarated = models.BooleanField(default=False)
    
    # it is been updated when statement and next_step of option has been changed and when genarate new report based on report 
    feedback_updated = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'    
    

    def notified(self):
        """
        Generate a visual indicator for notification based on the 'feedback_updated' status.
        
        If 'feedback_updated' is True, display a green background with "Updated" text.
        If 'feedback_updated' is False, display an orange background with "Pending" text.
        
        :return: HTML representation of the notification status.
        """
        if self.feedback_updated:
            return mark_safe('<b style="background:{};padding:5px;color:#ffffff;" >{}</b>'.format('green', self.feedback_updated))
        else:
            return mark_safe('<b style="background:{};padding:5px;color:#ffffff;" >{}</b>'.format('orange', 'Pending'))    

    def __str__(self):
        """
        Return a string representation of the object.

        :return: A string containing the name and ID of the object.
        """
        return str(self.name) + str(self.id)
    
    def get_absolute_url(self):
        """
        Get the absolute URL for the object, typically used for linking to its detailed view.

        :return: The absolute URL for the object.
        """
        return reverse('evaluation:nreport', args=[str(self.slug)])    
    
    def get_edit_url(self):
        """
        Get the absolute URL for the object, typically used for linking to its detailed view.

        :return: The absolute URL for the object.
        """
        return reverse('evaluation:edit_report', args=[str(self.slug)])    


class Evaluation(models.Model):
    '''    
    Automatically generated during evaluation by the user.
    Not displayed in the admin side.    
    '''
    evaluator = models.ForeignKey(Evaluator, on_delete=models.RESTRICT, related_name='eva_evaluator', db_index=True)
    option = models.ForeignKey(Option, on_delete=models.RESTRICT, related_name='eva_option')
    question = models.ForeignKey(Question, on_delete=models.RESTRICT,null=True, blank=True, related_name='eva_question')
    

    def __str__(self):
        return self.evaluator.name

    @property
    def get_question_comment(self):
        """
        Get comments associated with this evaluation's question.

        :return: QuerySet of comments for the question.
        """
        eva_comment = EvaComments.objects.filter(question = self.question, evaluator = self.evaluator)
        return eva_comment


class EvaComments(models.Model):
    '''    
    Automatically generated during evaluation by the user.
    Not displayed in the admin side.    
    '''
    evaluator = models.ForeignKey(Evaluator, on_delete=models.RESTRICT, related_name='coment_evaluator', db_index=True)
    question = models.ForeignKey(Question, on_delete=models.RESTRICT, related_name='comment_question', db_index=True)
    comments = models.TextField(max_length=600)

    def __str__(self):
        return self.comments


class EvaLabel(models.Model):
    '''    
    Automatically generated during evaluation by the user.
    Not displayed in the admin side.    
    '''
    label = models.ForeignKey(DifinedLabel, on_delete=models.PROTECT, related_name='labels', db_index=True)
    evaluator = models.ForeignKey(Evaluator, on_delete=models.RESTRICT, related_name='evaluators', db_index=True)
    sort_order = models.CharField(max_length=3, default=0)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.label.name

class EvaLebelStatement(models.Model):
    
    '''    
    Automatically generated during evaluation by the user.
    Not displayed in the admin side.    
    '''
    
    class Meta:
        verbose_name = 'Eva Label Statement'
        verbose_name_plural = 'Eva Label Statements'
    
    evalebel = models.ForeignKey(EvaLabel, on_delete=models.PROTECT, related_name='elabelstatement', db_index=True)
    question = models.ForeignKey(Question, on_delete=models.PROTECT, null=True, blank=True, related_name='evalabelques', db_index=True)
    option_id = models.CharField(max_length=252, null=True, blank=True)
    statement = models.TextField(blank=True, null=True)
    next_step = models.TextField(blank=True, null=True)
    positive = models.CharField(max_length=1, default=0, db_index=True)
    dont_know = models.BooleanField(default=False, db_index=True)
    assesment = models.BooleanField(default=False)
    next_activity = models.BooleanField(default=False)
    evaluator = models.ForeignKey(Evaluator, on_delete=models.RESTRICT, related_name='s_evaluators', null=True, db_index=True)    
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)

    def __str__(self):
        return self.statement
    @property
    def is_positive(self):
        """
        Check if the statement is positive.

        :return: True if positive, False otherwise.
        """
        if self.positive == str(1):
            return True
        return False
    @property
    def is_negative(self):
        """
        Check if the statement is negative.

        :return: True if negative, False otherwise.
        """
        if self.positive == str(0) and self.dont_know == False:
            return True
        return False
    
    @property
    def is_dontknow(self):
        """
        Check if the statement represents 'Don't Know'.

        :return: True if 'Don't Know', False otherwise.
        """
        if self.dont_know == True:
            return True
        return False
    

    
    
class NextActivities(models.Model):
    '''
    Main parameters for next activities.
    '''
    
    class Meta:
        verbose_name = 'Next Activity'
        verbose_name_plural = 'Next Activities'    

    name_and_standared = models.CharField(max_length=250)
    short_description = models.TextField(max_length=152)
    descriptions = models.TextField()
    url = models.URLField(null=True, blank=True)
    priority = models.CharField(max_length=2, help_text="To specify sort order!")
    related_questions = models.ManyToManyField(Question, related_name="related_next", verbose_name="Please select related questions to be answered by the test", help_text="Allow multiple option selection. The selected options should be highlighted.", limit_choices_to={'is_active': True}, db_index=True)
    compulsory_questions = models.ManyToManyField(Question, related_name="compulsory_next", verbose_name="Please select compulsory questions to be answered by the test", help_text="Allow multiple. The selected options should be highlighted.", limit_choices_to={'is_active': True}, db_index=True)
    related_percent = models.IntegerField(default=90)
    compulsory_percent = models.IntegerField(default=100)    
    is_active = models.BooleanField(default=True, verbose_name="Published?", help_text="Tick will published the service directly to the site!")
    same_tried_by = models.JSONField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='serviceby')
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)
    
    
    def __str__(self): 
        return str(self.name_and_standared)
    
    def get_quotations(self):        
        """
        Get quotations related to this next activity.

        :return: Quotations related to this next activity.
        """
        quotations = self.quotnextactivity.all()
        
        return set(quotations)    
    
    @property
    def related_questions_ids(self):      
        """
        Get the IDs of related questions.

        :return: IDs of related questions.
        """  
        return self.related_questions.all().values_list('id', flat= True).order_by('id')
    
    @property
    def compulsory_questions_ids(self):
        """
        Get the IDs of compulsory questions.

        :return: IDs of compulsory questions.
        """
        return self.compulsory_questions.all().values_list('id', flat= True).order_by('id')
    
    @property
    def selected_ids(self):
        """
        Get the IDs of selected questions (related and compulsory).

        :return: IDs of selected questions.
        """
        return (self.related_questions_ids.union(self.compulsory_questions_ids)).order_by('id')
    
    @property
    def answering_questions(self):
        """
        Get the questions that need to be answered for this next activity.

        :return: Questions to be answered.
        """
        return (self.related_questions.all()).union(self.compulsory_questions.all())
    
    @property
    def picked_experts(self):
        """
        Get the experts assigned to this next activity.

        :return: Experts assigned to this next activity.
        """
        from accounts.models import UsersNextActivity
        una_list = UsersNextActivity.objects.filter(next_activity = self)
        
        experts = [una.user for una in una_list if una.user.is_expert]
        
        return experts
                
    

class EvaluatorActivities(models.Model):
    """
    Model to represent Evaluator Activities.

    Attributes:
        evaluator (ForeignKey): The associated evaluator.
        next_activity (ForeignKey): The next activity related to the evaluator.
        related_percent (IntegerField): Related percentage.
        compulsory_percent (IntegerField): Compulsory percentage.
        is_active (BooleanField): Whether the activity is active or not.
        create_date (DateTimeField): Date and time of creation.
        update_date (DateTimeField): Date and time of the last update.

    Methods:
        __str__(): Returns a string representation of the next activity's name and standard.
    """
       
    evaluator = models.ForeignKey(Evaluator, on_delete=models.CASCADE, related_name="eaevaluator", db_index=True)    
    next_activity = models.ForeignKey(NextActivities, on_delete=models.CASCADE, related_name="eanextactivities")
    related_percent = models.IntegerField()
    compulsory_percent = models.IntegerField()
    is_active = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)
    
    def __str__(self):
        return str(self.next_activity.name_and_standared)
    
class OliList(models.Model):
    """
    Model to represent Defined Oils.

    Attributes:
        name (CharField): The name of the defined oil (unique).
        key (CharField): A unique key generated based on the name.

    Methods:
        __str__(): Returns the name of the defined oil.
        save(): Overrides the default save method to generate and save the key based on the name.
    """
    
    class Meta:
        verbose_name = 'Defined Oil'
        verbose_name_plural = 'Defined Oils'   
        
    name = models.CharField(max_length = 250, unique=True)
    key = models.CharField(null=True, blank=True, editable=False, max_length=250)    
    
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):  
        key_sample = slugify(self.name)    
        self.key = key_sample
        super(OliList, self).save(*args, **kwargs)
    
class StdOils(models.Model):    
    """
    Model to represent Standard Oils.

    Attributes:
        select_oil (ForeignKey): The selected oil from OliList.
        biofuel (ForeignKey): The associated biofuel (nullable).

    Methods:
        __str__(): Returns the name of the selected oil.
    """
    
    class Meta:
        verbose_name = 'Standard Oil'
        verbose_name_plural = 'Standard Oils'  
        
    select_oil = models.ForeignKey(OliList, on_delete=models.CASCADE, default=1)
    biofuel = models.ForeignKey(Biofuel, on_delete=models.SET_NULL, null=True, db_index=True)
    
    
    def __str__(self):
        return self.select_oil.name

class StandaredChart(models.Model):
    """
    Model to represent Standard Charts.

    Attributes:
        oil (ForeignKey): The associated standard oil.
        question (ForeignKey): The associated question.
        unit (ForeignKey): The associated weight unit (nullable).
        value (CharField): The value for the chart (nullable).
        link (URLField): A URL link (nullable).
        option (ChainedForeignKey): The associated option (nullable).

    Methods:
        oil_key(): Returns the lowercase key of the associated standard oil.
        __str__(): Returns the name of the associated standard oil.

    Note: Check the admin for this model, as options are overwritten to narrow down.
    """
    class Meta:
        verbose_name = 'Standard Chart'
        verbose_name_plural = 'Standard Charts'   
    
    from home.models import WeightUnit      
    from smart_selects.db_fields import ChainedForeignKey
    oil = models.ForeignKey(StdOils, on_delete=models.CASCADE,  related_name = 'std_oil_of_chart', db_index=True)    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="stanchart", limit_choices_to={'is_active': True}, db_index=True)
    unit = models.ForeignKey(WeightUnit, on_delete=models.CASCADE, related_name= "chrartunit", null=True, blank=True)
    value = models.CharField(max_length=252, null=True, blank=True)
    link = models.URLField(null=True, blank=True)   
    option = ChainedForeignKey(Option, chained_field="question", chained_model_field="question", show_all=False,auto_choose=True, sort=True, on_delete=models.SET_NULL, related_name='stoption', null=True, blank=True)
    
    
    @property
    def oil_key(self):
        return self.oil.selected_oil.key.lower() 
        
    def __str__(self):
        return self.oil.select_oil.name    
    

class Youtube_data(models.Model):
    """
    Model to store YouTube data for specific search terms.

    Attributes:
        term (TextField): The search term for YouTube data.
        urls (TextField): URLs related to the search term.
        create_date (DateTimeField): Date and time of creation.
        update_date (DateTimeField): Date and time of the last update.

    Methods:
        __str__(): Returns the search term as a string.
    """
    term = models.TextField()
    urls = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.term
    
class LabelDataHistory(models.Model):
    """
    Model to store Label Data History.

    Attributes:
        evaluator (ForeignKey): The associated evaluator.
        items (TextField): History of labeled items (limited to 250 characters).
        created (DateTimeField): Date and time of creation.

    Methods:
        __str__(): Returns the items history as a string.

    Meta:
        verbose_name = 'Label Data History'
        verbose_name_plural = 'Label Data Histories'
    """    
    
    class Meta:
        verbose_name = 'Label Data History'
        verbose_name_plural = 'Label Data Histories'        
    
    evaluator = models.ForeignKey(Evaluator, on_delete=models.CASCADE)  
    items= models.TextField(max_length=250)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.items    
    

class ReportMailQueue(models.Model):
    """
    Model to queue report mail sending tasks.

    Attributes:
        to (CharField): Email address of the recipient.
        from_report (ForeignKey): The sender (Evaluator) of the report.
        new_report (ForeignKey): The report being sent.
        added_at (DateTimeField): Date and time when the report was added to the queue.
        processed (BooleanField): Indicates whether the task has been processed.
        process_time (DateTimeField): Date and time of processing.
        tried (IntegerField): Number of attempts to send the report.

    Methods:
        __str__(): Returns the recipient's email address as a string.

    Note: The mail queues will be executed by crontab and are created during the saving of BlogPost.
    """
    to = models.CharField(max_length=256, null=True, blank=True)
    from_report = models.ForeignKey(Evaluator, on_delete=models.CASCADE, related_name='reportquefrom')   
    new_report = models.ForeignKey(Evaluator, on_delete=models.CASCADE, related_name='reportqueto')         
    added_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    process_time = models.DateTimeField(auto_now=True)
    tried=models.IntegerField(default=0)
    
    def __str__(self):
        return self.to
    
    
class Suggestions(models.Model):
    """
    Model to store user suggestions.

    Attributes:
        question (ForeignKey): The associated question (nullable).
        su_type (CharField): Type of suggestion ('question' or 'option').
        title (CharField): Title of the suggestion.
        statement (TextField): The suggestion statement.
        suggested_by (ForeignKey to User): The user who suggested the idea.
        parent (ForeignKey to self): The parent suggestion (nullable, used for replies).
        related_qs (ForeignKey to self): Related suggestion (nullable, for cross-reference).
        comitted (BooleanField): Indicates whether the suggestion has been committed.
        created (DateTimeField): Date and time of creation.
        updated (DateTimeField): Date and time of the last update.

    Methods:
        __str__(): Returns the title of the suggestion.

    Meta:
        verbose_name = 'Suggestion'

    Note: The 'question' field is nullable, allowing suggestions without an associated question.
    """  
    class Meta:        
        verbose_name = 'Suggestion'        
        
    TYPE_CHOICE = (
        ('question', 'Question'),
        ('option', 'Option'),
    )
    question = models.ForeignKey(Question, on_delete = models.SET_NULL, related_name='question_sugestion', null=True, blank=True, db_index=True)
    su_type = models.CharField(max_length=10, choices=TYPE_CHOICE, default='question')    
    title = models.CharField(max_length=252)
    statement = models.TextField()
    sugested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, related_name='sugestions')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies', db_index=True)
    related_qs = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='related', db_index=True)
    
    comitted =  models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    
 
    

    
