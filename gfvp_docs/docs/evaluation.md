# Welcome to The evaluation DOCS

## Apps layout

    Web Root        # The main folder of the web project.
        evaluation/
            templatestags #Written django's custom template tag to serve in the template
            admin.py
            apps.py
            forms.py
            helper.py  
            middleware # Custom Django's midleware  
            models.py
            nreport_class.py # Custom algorthm to build traffic-light overview
            signals.py
            tests.py
            urls.py
            views.py
            ...       

## Custom template Tags 

* `{% load custom_tags %}` - To load Custom template tags in the HTML file
* `{{ question.sort_order | brek_after_two}}` - To break line after first two word of the questions's sort order. It is not used now.
* `get_verbose_name(instance, field_name)` - It is using to build quotation report in function base view. It takes model instance and field name as parameter and return the verbose name of the field. It can be used in the template as well acroding tot he django's document.
* `in_quot(quote, user)` - This tag returns the quotations created by the user as service provider. Example use case: `{% if child.get_quotations|in_quot:user %}` to get all quotation of the user.

## Evaluation Admin

> Every class and features in the `admin.py` based on django's regular facility. Some exceptional in our case are mentoning here:

    class Media:
        css = {
            'all': (
                '/static/css/fancy.css',
            )
        } 

> Adding custom css using above code in admin class 

    change_list_template = 'admin/question_list.html'
    def changelist_view(self, request, extra_context=None):        
        questions = Question.objects.filter(is_active = True)
        label_pending_in_question = [q.sort_order for q in questions if not q.have_4labels]  
        problem_in_options =   [q.sort_order for q in questions if not q.problem_in_option]       
        extra_context = extra_context or {}
        extra_context['label_pending_in_question'] = label_pending_in_question
        extra_context['problem_in_options'] = problem_in_options        
        return super().changelist_view(request, extra_context=extra_context)  

> Adding error note using above by oerriding instance and method in the admin class of question.

    @admin.action(description='Genarate updated report and notify to the creator')
    def check_and_notify(self, request, queryset):
        from .views import set_evastatment, set_evastatement_of_logical_string
        ........
        .........
        ReportMailQueue.objects.create(
                to = i.email,
                from_report = i,
                new_report = copy_evaluator,
            )   

> Above method are adding action in Evaluator(Evaluator is the alternative coding name of human readable Report). The action should be called by admin on "Pening" marked report. Pending mark also a custom adition in admin interface which is described in the `models.py` in this documentation.

> Each call in above method create mail queue to send mail on next cronjob execution.


    class NextActivitiesAdmin(admin.ModelAdmin):  
        @admin.action(description='Duplicate Selected Activities')
        def duplicate_event(modeladmin, request, queryset):
            for object in queryset:
                ..........         
        actions = [duplicate_event]
    admin.site.register(NextActivities, NextActivitiesAdmin)
> Above aditional method in class creating a additional action to clone the selected objects in the `NextActivities` model in the admin side.


## APP

> App is a configuration file of evaluation app provided by Django. Here `signals.py` has been registered using below code. 

    def ready(self):
        import evaluation.signals

> Do not change anything in this file.


## Form

`forms.py` inheriting the default django's form class for evaluation initialization based on our CSS library. We are using `bootstrap 5`.