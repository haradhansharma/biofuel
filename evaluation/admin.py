'''
****Do not change anythings here
'''

from django.contrib import admin
from . models import *

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
admin.site.register(Evaluator, EvaluatorAdmin)

admin.site.register(DifinedLabel)
admin.site.register(Biofuel)
admin.site.register(Option)
admin.site.register(NextActivities)
admin.site.register(StandaredChart)





