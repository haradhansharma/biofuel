'''
****Do not change anythings here
'''

from django.contrib import admin
from . models import *
from django.contrib import messages
from django.utils.translation import ngettext
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail 
import uuid

class Labels(admin.TabularInline):
    model = Label
    extra = 0
    fk_name = "question"
    

class Options(admin.TabularInline):
    model = Option
    extra = 0 
    fk_name = "question"

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('sort_order', 'name', 'is_door',)
    list_filter = ('is_door','is_active',)
    inlines = [Labels, Options]
    
admin.site.register(Question, QuestionAdmin) 

class LsLabels(admin.TabularInline):
    model = Lslabel
    extra = 0
    fk_name = "logical_string"

class LogicalStringAdmin(admin.ModelAdmin):
    list_display = ('text',)
    inlines = [LsLabels]
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
        happen_time_restriction = 2
        #count happening   
        done = 0   
        #we will check only which report is genarated
        selected = queryset.filter(report_genarated = True)      
        if len(selected) > int(happen_time_restriction):  
            # if count is greater then parameter the nothing happend will show a warning message                  
            self.message_user(request, ngettext(  '%d Task can be done at a time to reduce overhelming.',  '%d Tasks can be done at a time to reduce overhelming.', happen_time_restriction, ) % happen_time_restriction, messages.WARNING)
        else:
            #do whatever want o do         
            
            mail_to_evaluator = []  
            current_site = Site.objects.get_current()   
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
                
                # send mail to the creator with update information    
                subject = f'Updated report #{copy_evaluator.id} with latest feedback based on #{i.id}' 
                message = render_to_string('emails/feedback_update.html', {
                            'copy_evaluator': copy_evaluator,                                                                                        
                            'domain': current_site.domain,    
                            'evaluator' : i        
                            }) 
                mail_to_evaluator.append((subject, message, settings.DEFAULT_FROM_EMAIL, [i.email]))
                
                
            #send all mail with one connection    
            send_mass_mail((mail_to_evaluator), fail_silently=False)
            
            #sucess message
            self.message_user(request, ngettext( '%d Task has been done based on genarated report and mail sent.',  '%d Tasks has been done based on genarated report and mail sent.', done, ) % done, messages.SUCCESS)
    actions = [check_and_notify]
     
    
    
    
admin.site.register(Evaluator, EvaluatorAdmin)

admin.site.register(DifinedLabel)
admin.site.register(Biofuel)
admin.site.register(Option)

admin.site.register(StandaredChart)



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






