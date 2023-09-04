'''
****Do not change anythings here
'''
# Import necessary modules and classes
from django.contrib import admin
from . models import *
from django.contrib import messages
from django.utils.translation import ngettext
import uuid
from import_export.admin import ExportActionMixin
from import_export import resources
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError


class LabelCheckFormset(BaseInlineFormSet):
    '''
    Custom formset class for labels inline.

    This formset is used to ensure that:
    - At least 4 labels are assigned to a question.
    - At least one label has the value '1' if the question's sort order is not '1'.

    Attributes:
        question (Question): The question associated with the labels.
    '''
    question = None
    def clean(self):
        super().clean()
        data = self.cleaned_data       
        if len(data) <  4:
            raise ValidationError("Please assign 4 labels")
        one_found = 0
        
        for d in data:
            value = d['value']
            self.question = d['question']
            if value == '1':
                one_found += 1
        if self.question.sort_order != 1:
            if one_found == 0:
                raise ValidationError("Atleast one label should have value 1")

        


class Labels(admin.TabularInline):
    '''
    Inline admin for Label model.

    This inline admin allows adding labels to a question when editing it in the admin panel.

    Attributes:
        model (Label): The Label model associated with this inline.
        extra (int): The number of extra label forms to display.
        fk_name (str): The foreign key name to associate labels with a question.
        formset (LabelCheckFormset): The custom formset to validate labels.
    '''
    model = Label
    extra = 0
    fk_name = "question"
    formset = LabelCheckFormset
    

class Options(admin.TabularInline):
    '''
    Inline admin for Option model.

    This inline admin allows adding options to a question when editing it in the admin panel.

    Attributes:
        model (Option): The Option model associated with this inline.
        extra (int): The number of extra option forms to display.
        fk_name (str): The foreign key name to associate options with a question.
    '''
    model = Option
    extra = 0 
    fk_name = "question"
    


class QuestionAdmin(ExportActionMixin, admin.ModelAdmin):
    '''
    Admin configuration for the Question model.

    This admin class configures the display and behavior of the Question model in the admin panel.

    Attributes:
        list_display (tuple): Fields to display in the list view of questions.
        list_filter (tuple): Fields to filter questions by.
        ordering (tuple): Fields to specify the default ordering of questions.
        inlines (list): Inline models (Labels and Options) to display when editing a question.
    '''
    list_display = ('id','sort_order', 'name', 'is_door',)
    list_filter = ('is_door','is_active',)
    ordering = ('sort_order',)
    inlines = [Labels, Options]     
       
    class Media:
        css = {
            'all': (
                '/static/css/fancy.css',
            )
        } 
        
    # To add error notes in the admin about question configuration
    change_list_template = 'admin/question_list.html'
    
    def changelist_view(self, request, extra_context=None):  
        '''
        Overrides the default changelist_view to add error notes to the admin panel.

        This method adds error notes about question configurations to the admin panel.
        It checks for questions with label issues, option issues, and is_door-related issues.

        Args:
            request (HttpRequest): The HTTP request object.
            extra_context (dict): Extra context to include in the view.

        Returns:
            HttpResponse: The HTTP response for the changelist view.
        '''      
        questions = Question.objects.filter(is_active = True)
        label_pending_in_question = [q.sort_order for q in questions if not q.have_4labels]  
        problem_in_options =   [q.sort_order for q in questions if not q.problem_in_option]    
        not_door_but_no_parent =   [q.sort_order for q in questions if q.not_is_door_nor_have_parent ]       
           
        extra_context = extra_context or {}
        extra_context['label_pending_in_question'] = label_pending_in_question
        extra_context['problem_in_options'] = problem_in_options      
        extra_context['not_door_but_no_parent'] = not_door_but_no_parent        
          
        return super().changelist_view(request, extra_context=extra_context)  
    
    
    def change_view(self, request, object_id, form_url='', extra_context=None):          
        '''
        Overrides the default change_view to customize the view for question editing.

        This method customizes the view for editing a question by modifying the behavior or appearance.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (str): The ID of the question being edited.
            form_url (str): The form URL.
            extra_context (dict): Extra context to include in the view.

        Returns:
            HttpResponse: The HTTP response for the change view.
        '''
        return super().change_view(request, object_id, form_url, extra_context=extra_context)    
    
# Register the Question model with its custom admin configuration
admin.site.register(Question, QuestionAdmin) 


class OptionResource(resources.ModelResource):
    class Meta:
        model = Option
        fields = ('name','question__name', 'next_question__name',)

class OptionAdmin(ExportActionMixin, admin.ModelAdmin): 
    '''
    Admin configuration for the Option model.

    This admin class configures the display and behavior of the Option model in the admin panel.

    Attributes:
        list_display (tuple): Fields to display in the list view of options.
        list_filter (tuple): Fields to filter options by.
        ordering (tuple): Fields to specify the default ordering of options.
        resource_class (OptionResource): The resource class for exporting options.
    '''   
    list_display = ('name', 'yes_status', 'dont_know', 'question', 'next_question',)
    list_filter = ('yes_status','dont_know', 'overall','positive', 'question', 'next_question', )   
    ordering = ('question', 'name',)
    # resource_class = OptionResource
    
admin.site.register(Option, OptionAdmin) 

class LsLabels(admin.TabularInline):
    '''
    Inline admin for Lslabel model.

    This inline admin allows adding labels to a logical string when editing it in the admin panel.

    Attributes:
        model (Lslabel): The Lslabel model associated with this inline.
        extra (int): The number of extra label forms to display.
        fk_name (str): The foreign key name to associate labels with a logical string.
        formset (LabelCheckFormset): The custom formset to validate labels.
    '''
    model = Lslabel
    extra = 0
    fk_name = "logical_string"
    formset = LabelCheckFormset
    
class StdOilsIn(admin.TabularInline):
    '''
    Inline admin for StdOils model.

    This inline admin allows adding standard oils to a biofuel when editing it in the admin panel.

    Attributes:
        model (StdOils): The StdOils model associated with this inline.
        extra (int): The number of extra standard oil forms to display.
        fk_name (str): The foreign key name to associate standard oils with a biofuel.
    '''
    model = StdOils
    extra = 0 
    fk_name = "biofuel"   
    
class BiofuelAdmin(admin.ModelAdmin):  
    '''
    Admin configuration for the Biofuel model.

    This admin class configures the display and behavior of the Biofuel model in the admin panel.

    Attributes:
        inlines (list): Inline models (StdOilsIn) to display when editing a biofuel.
    '''  
    inlines = [StdOilsIn]     
admin.site.register(Biofuel, BiofuelAdmin)

admin.site.register(OliList)
admin.site.register(LabelDataHistory)


class EvaLebelStatementAdmin(admin.ModelAdmin):
    '''
    Admin configuration for the EvaLebelStatement model.

    This admin class configures the display and behavior of the EvaLebelStatement model in the admin panel.

    Attributes:
        list_display (tuple): Fields to display in the list view of evaluation label statements.
        list_filter (tuple): Fields to filter evaluation label statements by.
    '''
    list_display = ('evalebel', 'question', 'option_id', 'positive', 'dont_know', 'evaluator', 'assesment',)
    list_filter = ('evalebel', 'evaluator', 'assesment' ,)   
admin.site.register(EvaLebelStatement, EvaLebelStatementAdmin)

class StandaredCharts(admin.TabularInline):
    '''
    Inline admin for StandaredChart model.

    This inline admin allows adding standard charts to an oil when editing it in the admin panel.

    Attributes:
        model (StandaredChart): The StandaredChart model associated with this inline.
        extra (int): The number of extra standard chart forms to display.
        raw_id_fields (tuple): Fields to display as raw IDs.
    '''
    model = StandaredChart
    extra = 0
    raw_id_fields = ("oil",)

    

class StdOilsAdmin(admin.ModelAdmin): 
    '''
    Admin configuration for the StdOils model.

    This admin class configures the display and behavior of the StdOils model in the admin panel.

    Attributes:
        list_display (tuple): Fields to display in the list view of standard oils.
        inlines (tuple): Inline models (StandaredCharts) to display when editing a standard oil.
    '''
    list_display = ('select_oil', 'biofuel',)
    inlines = (
        StandaredCharts,
        )  
    
    class Media:
        css = {
            'all': (
                '/static/css/fancy.css',
            )
        } 
admin.site.register(StdOils, StdOilsAdmin)

class SuggestionsAdmin(admin.ModelAdmin): 
    '''
    Admin configuration for the Suggestions model.

    This admin class configures the display and behavior of the Suggestions model in the admin panel.

    Attributes:
        list_display (tuple): Fields to display in the list view of suggestions.
        list_filter (tuple): Fields to filter suggestions by.
        search_fields (tuple): Fields to search suggestions by.
        ordering (tuple): Fields to specify the default ordering of suggestions.
        readonly_fields (tuple): Fields to mark as read-only in the admin panel.
    '''
    list_display = ('su_type','title', 'statement', 'sugested_by', 'related_qs', 'question', 'comitted',)
    list_filter = ('su_type', 'comitted', 'question', )
    search_fields = ('title', 'statement', 'question', )   
    ordering = ('updated',)
    readonly_fields = ('su_type','question','sugested_by', 'parent', 'related_qs' )     
admin.site.register(Suggestions, SuggestionsAdmin)



class LogicalStringAdmin(admin.ModelAdmin):
    '''
    Admin configuration for the LogicalString model.

    This admin class configures the display and behavior of the LogicalString model in the admin panel.

    Attributes:
        list_display (tuple): Fields to display in the list view of logical strings.
        inlines (tuple): Inline models (LsLabels) to display when editing a logical string.
        list_filter (tuple): Fields to filter logical strings by.
        change_list_template (str): The template for the changelist view.
    '''
    list_display = ('option_list', 'text', 'overall', 'positive', 'Label_value_one_to', )
    inlines = [LsLabels]
    list_filter = ('overall', 'positive' ,)   
    
    # To add error notes in the admin about question configuration 
    change_list_template = 'admin/logical_string_list.html'
    
    def changelist_view(self, request, extra_context=None):   
        '''
        Overrides the default changelist_view to add error notes to the admin panel.

        This method adds error notes about logical string configurations to the admin panel.
        It checks for logical strings with label issues.

        Args:
            request (HttpRequest): The HTTP request object.
            extra_context (dict): Extra context to include in the view.

        Returns:
            HttpResponse: The HTTP response for the changelist view.
        '''     
        strings = LogicalString.objects.all()
        label_pending_in_logical_string = [ls.option_list for ls in strings if not ls.have_4labels]     
        extra_context = extra_context or {}
        extra_context['label_pending_in_logical_string'] = label_pending_in_logical_string  
          
        return super().changelist_view(request, extra_context=extra_context)  
admin.site.register(LogicalString, LogicalStringAdmin)


class EvaluatorAdmin(admin.ModelAdmin): 
    '''
    Admin configuration for the Evaluator model.

    This admin class configures the display and behavior of the Evaluator model in the admin panel.

    Attributes:
        list_display (tuple): Fields to display in the list view of evaluators.
        list_filter (tuple): Fields to filter evaluators by.
        readonly_fields (tuple): Fields to mark as read-only in the admin panel.
    '''
      
    list_display = ('id', 'notified', 'name','creator', 'email', 'phone', 'biofuel', 'create_date','orgonization', 'report_genarated')
    list_filter = ('biofuel', )
    readonly_fields = ('report_genarated', 'orgonization', 'name','creator', 'email', 'phone', 'biofuel', 'create_date', 'id')   
    
    
    @admin.action(description='Genarate updated report and notify to the creator')    
    def check_and_notify(self, request, queryset):
        '''
        Custom admin action to generate updated reports and notify the creators.

        This action duplicates selected evaluators, generates updated reports, and sends notifications.

        Args:
            request (HttpRequest): The HTTP request object.
            queryset (QuerySet): The queryset of selected evaluators.
        '''
        from .views import set_evastatment, set_evastatement_of_logical_string    
        
        done = 0   
 
        selected = queryset.filter(report_genarated = True)      
       
        for i in selected:         
            
            done += 1
            
            # We are marking as updated to change in both to original and copied
            i.feedback_updated = True
            i.save()
            
            #copy current evaluator                
            copy_evaluator = Evaluator.objects.get(pk = i.pk)
            copy_evaluator.pk = None
            copy_evaluator.slug = uuid.uuid4()
            copy_evaluator.save()
            
            #copy evalabel
            evalabels = EvaLabel.objects.filter(evaluator = i)
            for el in evalabels:
                el.pk = None
                el.evaluator = copy_evaluator
                el.save()
                
            #copy eva comments
            evacomments = EvaComments.objects.filter(evaluator = i)
            for ec in evacomments:
                ec.pk = None
                ec.evaluator = copy_evaluator
                ec.save()
                            
            #copy evaluation
            evaluations = Evaluation.objects.filter(evaluator = i)
            for e in evaluations:
                e.pk = None
                e.evaluator = copy_evaluator
                e.save()
            
            #regenarate statement baed on options
            evastatement_options = EvaLebelStatement.objects.filter(evaluator = i, option_id__isnull = False) 
            for eo_id in list(set(eo.option_id for eo in evastatement_options)):  
                set_evastatment(request, Option.objects.get(id = int(eo_id)), copy_evaluator)
                set_evastatement_of_logical_string(request, Option.objects.get(id = int(eo_id)), copy_evaluator)
                
            ReportMailQueue.objects.create(
                to = i.email,
                from_report = i,
                new_report = copy_evaluator,
            )   
             
        #sucess message
        self.message_user(request, ngettext( f'{done} mail has been queued.'), messages.SUCCESS)
        
    actions = [check_and_notify]    
admin.site.register(Evaluator, EvaluatorAdmin)

admin.site.register(DifinedLabel)
admin.site.register(ReportMailQueue)

class StandaredChartAdmin(admin.ModelAdmin):
    '''
    Admin configuration for the StandaredChart model.

    This admin class configures the display and behavior of the StandaredChart model in the admin panel.

    Attributes:
        list_display (tuple): Fields to display in the list view of standard charts.
        list_editable (tuple): Fields that can be edited directly in the list view.
        list_display_links (tuple): Fields to display as links in the list view.
        list_filter (tuple): Fields to filter standard charts by.
        ordering (tuple): Fields to specify the default ordering of standard charts.
        list_per_page (int): Number of standard charts to display per page in the list view.
    '''
    list_display = ('id','question','oil', 'option', 'value', 'link',  )
    list_editable = ('oil', 'link', 'option', 'value', 'question',)
    list_display_links = ('id',)
    list_filter = ('question', )
    ordering = ('question',)
    list_per_page = 10
    
    
    class Media:
        css = {
            'all': (
                '/static/css/fancy.css',
            )
        }   
admin.site.register(StandaredChart, StandaredChartAdmin)

class NextActivitiesAdmin(admin.ModelAdmin): 
    '''
    Admin configuration for the NextActivities model.

    This admin class configures the display and behavior of the NextActivities model in the admin panel.

    Attributes:
        readonly_fields (tuple): Fields to mark as read-only in the admin panel.
    ''' 
    @admin.action(description='Duplicate Selected Activities')
    def duplicate_event(modeladmin, request, queryset):
        for object in queryset:
            related_questions = object.related_questions.all()
            compulsory_questions = object.compulsory_questions.all()
            object.id = None
            
            object.save()
            object.related_questions.set(related_questions)
            object.compulsory_questions.set(compulsory_questions)            
    actions = [duplicate_event]
    readonly_fields = ('same_tried_by', ) 
admin.site.register(NextActivities, NextActivitiesAdmin)






