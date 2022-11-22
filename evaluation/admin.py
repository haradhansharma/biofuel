'''
****Do not change anythings here
'''

from django.contrib import admin
from home.models import WeightUnit
from . models import *
from django.contrib import messages
from django.utils.translation import ngettext
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail 
import uuid
from import_export.admin import ExportActionMixin
from import_export import resources
from django import forms

class Labels(admin.TabularInline):
    model = Label
    extra = 0
    fk_name = "question"
    

class Options(admin.TabularInline):
    model = Option
    extra = 0 
    fk_name = "question"
    


class QuestionAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('sort_order', 'name', 'is_door',)
    list_filter = ('is_door','is_active',)
    ordering = ('sort_order',)
    inlines = [Labels, Options]        
    class Media:
        css = {
            'all': (
                '/static/css/fancy.css',
            )
        } 
        
    # to add error note in the admi about question configuration 
    change_list_template = 'admin/question_list.html'
    def changelist_view(self, request, extra_context=None):        
        questions = Question.objects.filter(is_active = True)
        label_pending_in_question = [q.sort_order for q in questions if not q.have_4labels]  
        problem_in_options =   [q.sort_order for q in questions if not q.problem_in_option]       
        extra_context = extra_context or {}
        extra_context['label_pending_in_question'] = label_pending_in_question
        extra_context['problem_in_options'] = problem_in_options        
        return super().changelist_view(request, extra_context=extra_context)  
    
    def change_view(self, request, object_id, form_url='', extra_context=None):          
        # oi = object_id.sort_order
        return super().change_view(request, object_id, form_url, extra_context=extra_context)    
admin.site.register(Question, QuestionAdmin) 


class OptionResource(resources.ModelResource):
    class Meta:
        model = Option
        fields = ('name','question__name', 'next_question__name',)

class OptionAdmin(ExportActionMixin, admin.ModelAdmin):    
    list_display = ('name', 'yes_status', 'dont_know', 'question', 'next_question',)
    list_filter = ('yes_status','dont_know', 'overall','positive', 'question', 'next_question', )   
    ordering = ('question', 'name',)
    # resource_class = OptionResource
admin.site.register(Option, OptionAdmin) 

class LsLabels(admin.TabularInline):
    model = Lslabel
    extra = 0
    fk_name = "logical_string"
    
class StdOilsIn(admin.TabularInline):
    model = StdOils
    extra = 0 
    fk_name = "biofuel"   
    
class BiofuelAdmin(admin.ModelAdmin):    
    inlines = [StdOilsIn]     
admin.site.register(Biofuel, BiofuelAdmin)

admin.site.register(OliList)
admin.site.register(LabelDataHistory)
# admin.site.register(EvaLebelStatement)

class EvaLebelStatementAdmin(admin.ModelAdmin):
    list_display = ('evalebel', 'question', 'option_id', 'positive', 'dont_know', 'evaluator', 'assesment',)
    list_filter = ('evalebel', 'evaluator', 'assesment' ,)   
    
    
admin.site.register(EvaLebelStatement, EvaLebelStatementAdmin)

class StandaredCharts(admin.TabularInline):
    model = StandaredChart
    extra = 0
    # fk_name = 'oil'
    raw_id_fields = ("oil",)

    

class StdOilsAdmin(admin.ModelAdmin): 
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



class LogicalStringAdmin(admin.ModelAdmin):
    list_display = ('option_list', 'text', 'overall', 'positive', 'Label_value_one_to', )
    inlines = [LsLabels]
    list_filter = ('overall', 'positive' ,)   
    
        
admin.site.register(LogicalString, LogicalStringAdmin)


class EvaluatorAdmin(admin.ModelAdmin): 
      
    list_display = ('id', 'notified', 'name','creator', 'email', 'phone', 'biofuel', 'create_date','orgonization', 'report_genarated')
    list_filter = ('biofuel', )
    readonly_fields = ('report_genarated', 'orgonization', 'name','creator', 'email', 'phone', 'biofuel', 'create_date', 'id')   
    
    
    @admin.action(description='Genarate updated report and notify to the creator')
    def check_and_notify(self, request, queryset):
        from .views import set_evastatment, set_evastatement_of_logical_string
        
        '''
        if no date in database then fill dummy date to execute well.       
        
        '''   
        
        
        #parameter to be happend check and send mail
        # happen_time_restriction = 50
        #count happening   
        done = 0   
        #we will check only which report is genarated
        selected = queryset.filter(report_genarated = True)      
        # if len(selected) > int(happen_time_restriction):  
        #     # if count is greater then parameter the nothing happend will show a warning message                  
        #     self.message_user(request, ngettext(  '%d Task can be done at a time to reduce overhelming.',  '%d Tasks can be done at a time to reduce overhelming.', happen_time_restriction, ) % happen_time_restriction, messages.WARNING)
        # else:
        #     #do whatever want o do         
            
        # mail_to_evaluator = []  
        # current_site = Site.objects.get_current()   
        for i in selected:
            #counting
            
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

# admin.site.register(Option)



class StandaredChartAdmin(admin.ModelAdmin):
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
    
    
    
    # change_form_template = 'admin/oil_change_form.html'
    
        
    
    # to exclude option field if no question selected
    # def get_fields(self, request, obj=None):
    #     if obj is None:
    #         '''
    #         If creating new from admin interface then the option field we will keep hide
    #         '''
    #         context = ('oil', 'question', 'unit', 'value', 'link')
    #     else:
    #         context = super().get_fields(request, obj)         
    #     return context
    
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     obj_id = request.resolver_match.kwargs.get('object_id')
    #     try:
    #         '''
    #         As we are overwriting default behaviour then we will delete the option if no question is there, this is essential during editing
    #         '''
    #         obj = StandaredChart.objects.get(id = int(obj_id))            
    #         if not obj.question:
    #             obj.option = None
    #             obj.save()
    #     except:
    #         obj = None
        
    #     if db_field.name == "option":
    #         '''
    #         Pverwriting option field to narrow down based on selected question.
    #         '''
    #         kwargs["queryset"] = Option.objects.filter(question = obj.question if obj else None)           
    #     return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    # def add_view(self, request, form_url='', extra_context=None):
    #     '''
    #     Show only sve and continue in admin inerface on addition form
    #     '''
        
    #     extra_context = extra_context or {}
    #     extra_context['show_save'] = False # Here
    #     extra_context['show_save_and_continue'] = True # Here        
    #     extra_context['show_save_and_add_another'] = False # Here
    #     return super().add_view(request, form_url, extra_context)
    # def change_view(self, request, object_id, form_url='', extra_context=None):   
        
    #     objects = StandaredChart.objects.all()
    #     object = objects.get(id = object_id)        
    #     oil = object.oil
    #     # obj_having_this_question = objects.filter(oil = oil)        
    #     # extra_context = extra_context or {}
    #     # extra_context['questions'] = [q.question for q in obj_having_this_question]
    #     return super().change_view(request, object_id, form_url, extra_context=extra_context)
        
admin.site.register(StandaredChart, StandaredChartAdmin)

class NextActivitiesAdmin(admin.ModelAdmin):  
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
admin.site.register(NextActivities, NextActivitiesAdmin)






