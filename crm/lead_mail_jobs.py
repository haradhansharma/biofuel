from .models import MailQueue, Lead
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mass_mail 
from django.utils import timezone 

CURRENT = timezone.now()

def last_process_time():
    
    pendings = MailQueue.objects.all().order_by('process_time').first()        
    return pendings.process_time 
    
def total_mail_sent():
    
    return  MailQueue.objects.filter(processed = True).count()       
    

def pending_queue_count():
    try:        
        return MailQueue.objects.filter(processed = False).count()
    except:
        return 0


def send_lead_mail():
    
    
    if ((CURRENT - last_process_time()).seconds) > settings.EXECUT_MAIL_IN_SECONDS or ((CURRENT - last_process_time()).seconds/60/60) == 0:
        
        
        pendings = MailQueue.objects.filter(processed = False).order_by('-added_at')[:settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME]   
        current_site = Site.objects.get_current()   
        subject = current_site.domain + ' miss you!'
        
        
        mail_to_lead = []    
        for pending in pendings:
            try:
                lead = Lead.objects.get(email_address = pending.to)       
                message = render_to_string('emails/crm_initial_mail.html', {
                            'confirm_code': lead.confirm_code,
                            'lead' : lead,                                                               
                            'domain': current_site.domain,            
                            }) 
                mail_to_lead.append((subject, message, settings.DEFAULT_FROM_EMAIL, [pending.to]))
                            
                pending_to_this = MailQueue.objects.get(to = pending.to, processed = False)
                pending_to_this.tried += 1       
                pending_to_this.processed = True
                pending_to_this.process_time = CURRENT
                pending_to_this.save()
            except:
                pass
        #send bulk mail using only one conenction
        send_mass_mail((mail_to_lead), fail_silently=False)
        
        MailQueue.objects.filter(tried__gt = 2).delete()
    
    return total_mail_sent()

