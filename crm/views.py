import csv
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from gfvp import null_session
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
import random
from django.contrib.sites.models import Site
from django.contrib import messages
from .forms import UploadLead
from django.core.files.storage import default_storage
import os
from .lead_mail_jobs import pending_queue_count, send_lead_mail
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from doc.models import Acordion


def mail_schedule(request):
    total_mail = send_lead_mail()
    return HttpResponse( f"Total {total_mail} Mail sent to the lead!" )
    


#helper function
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

@staff_member_required
def leads(request):
    #default behavior to avoid error
    null_session(request)
    print( request.POST)
    
    #Post method event    
    if request.method == "POST": 
        
        
        '''Lead delete method'''
        if 'delete_lead' in request.POST:
            #If no data selected return
            if not request.POST.getlist('lead'):
                messages.warning(request, "Please select lead")
                return HttpResponseRedirect(reverse('crm:leads')) 
            #get selected data 
            lead_ids = request.POST.getlist('lead')
            #delete selected lead   
            delete_count = 0         
            for li in lead_ids:
                Lead.objects.get(id = li).delete()
                delete_count += 1
            messages.success(request, f"{ delete_count } lead deleted successfully.")
                   
        
        '''lead to queue to sent later. 50 lead can be added at a time. it can be adjusted form setting file. But More then 50 site can be slow.'''
        if 'mail_lead' in request.POST:
            
            #IF unsent more then setting value in the queue no lead will be added to the queue
            if pending_queue_count() >= settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME:
                messages.warning(request, f"There are {pending_queue_count()} mail in queue! The command can be proccessed if queue less then {settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME}")
                return HttpResponseRedirect(reverse('crm:leads'))   
                            
            #If no data selected return
            if not request.POST.getlist('lead'):
                messages.warning(request, "Please select lead")
                return HttpResponseRedirect(reverse('crm:leads'))   
            
            #Allowed limited email per action to reduce RAM load
            if len(request.POST.getlist('lead')) > settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME:
                messages.warning(request, "Please select less then 50! " + "There was " + str(len(request.POST.getlist('lead'))) + " selected!" )
                return HttpResponseRedirect(reverse('crm:leads'))       
            
            #get selected datalist
            lead_ids = request.POST.getlist('lead')  
            
            # If no qualified lead found system will redirect.
            try:      
                result_lead = Lead.objects.filter(pk__in = lead_ids, subscribed = True) 
            except:
                messages.warning(request, "No Subscribed lead found")
                return HttpResponseRedirect(reverse('crm:leads'))  
            
            
            process_count = 0
            pending_in_queue = 0
            for rl in result_lead:            
                
                #To protect to be unsubscribe lead by robotic action
                try:
                    pending_exists = MailQueue.objects.filter(to = rl.email_address, processed = False).count()
                except:
                    pending_exists = 0
                    
                if pending_exists == 0:     
                    confirm_code = random_digits()
                    lead = Lead.objects.get(email_address = rl.email_address)
                    lead.confirm_code = confirm_code
                    lead.save() 
                    
                    process_count += 1                    
                    
                    #save to mail queue                
                    que = MailQueue(to = rl.email_address)
                    que.save()
                else:
                    pending_in_queue += 1                
                
                
            messages.success(request, f"{process_count} Mail processed successfully in mail queue and {pending_in_queue} mail still exists in queue to sent. Mail in queue has not been queued yet!")
            
        '''Save lead form CSV file'''    
        if 'lead_upload' in request.FILES:
            
            upload_csv_form = UploadLead(request.POST, request.FILES)
            
            if upload_csv_form.is_valid():
                
                lead_upload = upload_csv_form.cleaned_data['lead_upload'] 
                #alow only csv
                if not lead_upload.name.endswith('.csv'):
                    messages.error(request, 'File is not CSV type! Pleas Save your excel file in .csv format')
                    return HttpResponseRedirect(reverse('crm:leads'))  
                
                #protect to extra large
                if lead_upload.multiple_chunks():
                    messages.error(request, 'Uploaded file is too big (%.2f MB)' %(lead_upload.size(1000*1000),))
                    return HttpResponseRedirect(reverse('crm:leads'))  
                
                
                data = csv.DictReader(chunk.decode() for chunk in lead_upload)
                
                entry_count = 0
                error_count = 0                
                for d in data:                    
                    try:
                        new_lead = Lead(lead = str(d['lead']), email_address = str(d['email_address']), phone = str(d['phone']), address_1 = str(d['address_1']), address_2 = str(d['address_2']), country = str(d['country_code']), city = str(d['city']))
                        new_lead.save()
                        entry_count += 1
                    except Exception as e:
                        error_count += 1
                messages.success(request, f'{entry_count} lead has beed added! \n')
                messages.error(request, f"\n There was {error_count} error! Please check file format, record's title and duplicate email before each upload! \n")            
            
    upload_csv_form = UploadLead()
    
        
    #List of Leads
    leads = Lead.objects.all().order_by('lead')
    
    #pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(leads, 50)
    try:
        leads = paginator.page(page)
    except PageNotAnInteger:
        leads = paginator.page(1)
    except EmptyPage:
        leads = paginator.page(paginator.num_pages)
    
    docs = Acordion.objects.filter(apps = 'crm')
    
    context = {        
        'leads': leads,
        'upload_csv_form': upload_csv_form,
        'docs': docs,
        'EXECUT_MAIL_IN_SECONDS': settings.EXECUT_MAIL_IN_SECONDS
    }
    return render(request, 'crm/leads.html', context = context)

def unsubscrib(request, **kwargs):  
    
    try:  
        lead = Lead.objects.get(email_address = kwargs['email'], confirm_code = kwargs['code'])
        lead.subscribed = False
        lead.save()    
    except:
        messages.warning(request, "No email found!")
        return HttpResponseRedirect(reverse('home:home'))        
        
        
    return render(request, 'crm/unsubscribed.html', {'lead': lead, 'action': 'unsubscribed'})

def subscrib(request, **kwargs):    
    try:
        lead = Lead.objects.get(email_address = kwargs['email'])
        lead.subscribed = True
        lead.save()    
    except:
        messages.warning(request, "No email found!")
        return HttpResponseRedirect(reverse('home:home'))      
        
    return render(request, 'crm/subscribed.html', {'lead': lead, 'action': 'subscribed'})


             
    