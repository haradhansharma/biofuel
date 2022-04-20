from django.apps import AppConfig


class CrmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crm'
    
    # def ready(self):
    #     # from jobs.updater import ScheduleParse, SendNewsLatter    
    #     from . lead_mail_jobs import send_lead_mail   
        
    #     send_lead_mail()
