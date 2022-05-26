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
    list_display = ('name','creator', 'email', 'phone', 'biofuel', 'create_date','orgonization', 'report_genarated')
    list_filter = ('biofuel', )
    readonly_fields = ('report_genarated', 'orgonization', 'name','creator', 'email', 'phone', 'biofuel', 'create_date',)
    
    
    @admin.action(description='Check changes in evaluations and notify to the evaluators')
    def check_and_notify(self, request, queryset):
        
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
            for i in selected:
                #counting
                done += 1    
                
                
                changed_statement = []   
                current_site = Site.objects.get_current()   
                subject = f'Feedback changed in your report #{i.id}' 
                message = render_to_string('emails/feedback_update.html', {
                            'changed_statement': changed_statement,                                                                                        
                            'domain': current_site.domain,    
                            'evaluator' : i        
                            }) 
                
                #check and update feedback of this report
                statement_of_report = EvaLebelStatement.objects.filter(evaluator = i, option_id__gt = 0)                
                for sor in statement_of_report:  
                    get_option_feedback = Option.objects.get(id = int(sor.option_id))
                    if get_option_feedback.statement != sor.statement:
                        sor.statement = get_option_feedback.statement
                        sor.save()
                        changed_statement.append(sor)    
                        
                print(changed_statement)  
                mail_to_evaluator.append((subject, message, settings.DEFAULT_FROM_EMAIL, [i.email]))
            send_mass_mail((mail_to_evaluator), fail_silently=False)
                        
                        
                    
                    
                
            
            
            #sucess message
            self.message_user(request, ngettext( '%d Task has been done based on genarated report and mail sent.',  '%d Tasks has been done based on genarated report and mail sent.', done, ) % done, messages.SUCCESS)
            
        
        
        
       
                
        
                
                
        
        
        
    
    
    actions = [check_and_notify]
     
    
    
    
admin.site.register(Evaluator, EvaluatorAdmin)

admin.site.register(DifinedLabel)
admin.site.register(Biofuel)
admin.site.register(Option)
admin.site.register(NextActivities)
admin.site.register(StandaredChart)





