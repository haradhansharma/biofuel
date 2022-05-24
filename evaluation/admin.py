'''
****Do not change anythings here
'''

from django.contrib import admin
from . models import *
from django.contrib import messages
from django.utils.translation import ngettext

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
        happened = 0 
        happen_time_restriction = 3   
        for i in queryset:
            happened += 1
            if happened <= happen_time_restriction:               
                self.message_user(request, ngettext( '%d Task has been done and mail sent.',  '%d Tasks has been done and mail sent.', happen_time_restriction, ) % happen_time_restriction, messages.SUCCESS)
            else:
                self.message_user(request, ngettext(  '%d Task can be done at a time to reduce overhelming.',  '%d Tasks can be done at a time to reduce overhelming.', happen_time_restriction, ) % happen_time_restriction, messages.WARNING)
        
                
                
        
        
        
    
    
    actions = [check_and_notify]
     
    
    
    
admin.site.register(Evaluator, EvaluatorAdmin)

admin.site.register(DifinedLabel)
admin.site.register(Biofuel)
admin.site.register(Option)
admin.site.register(NextActivities)
admin.site.register(StandaredChart)





