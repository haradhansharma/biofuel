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
from .lead_mail_jobs import pending_queue_count, send_lead_mail, last_process_time, CURRENT, SendQueueMail
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from doc.models import Acordion
from django.utils import timezone 
from crm.forms import SubscriberForm
import urllib.request
import json
from django_countries import countries
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site

import logging
log =  logging.getLogger('log')

#helper function to create confirm code
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

#helper function to get ip address
def get_ip(request):
    log.info('Recording users IP............')
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:        
        ip = x_forwarded_for.split(',')[-1].strip()    
    elif request.META.get('HTTP_CLIENT_IP'):        
        ip = request.META.get('HTTP_CLIENT_IP')
    elif request.META.get('HTTP_X_REAL_IP'):        
        ip = request.META.get('HTTP_X_REAL_IP')
    elif request.META.get('HTTP_X_FORWARDED'):        
        ip = request.META.get('HTTP_X_FORWARDED')
    elif request.META.get('HTTP_X_CLUSTER_CLIENT_IP'):        
        ip = request.META.get('HTTP_X_CLUSTER_CLIENT_IP')
    elif request.META.get('HTTP_FORWARDED_FOR'):        
        ip = request.META.get('HTTP_FORWARDED_FOR')
    elif request.META.get('HTTP_FORWARDED'):        
        ip = request.META.get('HTTP_FORWARDED')
    elif request.META.get('HTTP_VIA'):        
        ip = request.META.get('HTTP_VIA')    
    else:        
        ip = request.META.get('REMOTE_ADDR')
    
    log.info(f'Ip found {ip} ')
        
    return ip

#get ip location using ipinfo database's free token whenre has 50k query free per month.
def get_location_info(request):
    log.info('Geting Location details based on IP')
    ip = get_ip(request)
    token = '6ef5b9c92955e8'
    info_url = f'https://ipinfo.io/{ip}?token={token}'
    data = {}
    with urllib.request.urlopen(info_url) as url:
        data =  json.loads(url.read().decode())
        data.update(data)
    log.info(f'Location data {data} found for user {request.user} ')
    return data
    

def subscription(request):
    '''
    To Subscribe newsletter need to supply Name and email address in correct formate.
    If email wrong then function will give error to the user
    Firstly System will check the supplied email already exists or not
    If email exists and subscription status is true then will show email already subscribed
    If email exists and subscription status is false then will send email for subscription confirm.
    If email is not exists new lead will save and confirmation mail will send by system
    Response will return by HTMX technology so we are returning HTTPResponse.
    
    '''
    location_info = get_location_info(request)
    subscription_form = SubscriberForm()
    name= None    
    email = None   
    city =  location_info.get('city') 
    country_code = location_info.get('country')
    country = country_code
    domain = get_current_site(request).domain
    
    if request.method == 'POST':
        log.info('Subscription form submitted')        
        if 'new_subscriber' in request.POST:
            log.info('Somebody want to subscribe to our newsletter!')
            subscription_form = SubscriberForm(request.POST)
            if subscription_form.is_valid():
                log.info('Subscription Form Submitted successfully!')
                name = subscription_form.cleaned_data['name']                
                email = subscription_form.cleaned_data['email']
                confirm_url = request.build_absolute_uri(reverse('crm:subscrib', kwargs={'email': email}))                    
                subject = 'Please confirm your subscription!'
                message = f'Hi {name}, <br> Thank you for subscription request to our newsletter. <br> Please confirm your subscription by clicking the link below... <br> {confirm_url} <br> With Thanks <br><br> {domain} Team.'
                email_from = settings.DEFAULT_FROM_EMAIL
                email_to = [email]
                
                try:
                    lead = Lead.objects.get(email_address = email)  
                    log.info('Tried email for subscription already exists')                 
                except Exception as e:
                    log.info('Going to record new subscription')
                    lead = None
                    
                if lead is not None:
                    if lead.subscribed:
                        return HttpResponse(f' <span class="text-danger"> The {email} already subscribed! </span>')
                    else: 
                        log.info('But the requested email is not confirmed! So that confirmation mail sending!')                       
                        send_mail(subject, message, email_from, email_to )   
                        log.info(f'Confirmation Email sent to the email {email} ')                     
                        return HttpResponse(f' <span class="text-danger"> An email for confirmation has been sent to {email} ! Please confirm! </span>')
                else:
                    try:
                        log.info(f'{email} saving as new lead! ')
                        Lead.objects.create(lead = name, email_address=email,city=city,country=country,subscribed=False)
                        log.info(f'{email} created as new lead!')
                    except Exception as e:
                        log.warning(f'There was a problem to save {email} as new lead due to {e}')
                    
                    log.info('Confirmation mail sending to new lead')    
                    send_mail(subject, message, email_from, email_to ) 
                    log.info('Confirmation mail sent to new lead!')
                    return HttpResponse(f' <span class="text-danger"> An email for confirmation has been sent to {email} ! Please confirm! </span>')
            else:
                log.warning(f'Wrong data found during subscription!')
                return HttpResponse(f' <span class="text-danger">Please check email is correctly written! </span>')
                
    log.warning(f'Something wrong during subscription process!')
    return HttpResponse(f' <span class="text-danger"> Soemthing Wrong! </span>')
                    
                        
                        
                
                

@login_required
@staff_member_required
def leads(request):
    #default behavior to avoid error
    null_session(request)   
    #Post method event    
    if request.method == "POST":        
        '''Lead delete method'''
        if 'delete_lead' in request.POST:
            log.info('Initializing lead deleting action from frontend...........')
            #If no data selected return
            if not request.POST.getlist('lead'):
                messages.warning(request, "Please select lead")
                log.info('No lead selected to delete so that redirecting.....')
                return HttpResponseRedirect(reverse('crm:leads')) 
            #get selected data 
            lead_ids = request.POST.getlist('lead')
            #delete selected lead   
            delete_count = 0       
            log.info(f"deleting selected leads by {request.user} ........")  
            for li in lead_ids:
                Lead.objects.get(id = li).delete()
                delete_count += 1
            messages.success(request, f"{ delete_count } lead deleted successfully.")
            log.info(f"{ delete_count } lead deleted successfully by {request.user}.")
                   
        
        '''lead to queue to sent later. settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME lead can be added at a time. it can be adjusted form setting file. But More then 50 site can be slow.'''
        if 'mail_lead' in request.POST:            
            #IF unsent more then setting value in the queue no lead will be added to the queue
            if pending_queue_count() >= settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME:
                mgs_string_for_mail_lead = f"There are {pending_queue_count()} mail in queue! The command can be proccessed if queue less then {settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME}!"
                messages.warning(request, mgs_string_for_mail_lead )
                log.info(str(mgs_string_for_mail_lead) + str('so that redirecting...........'))
                return HttpResponseRedirect(reverse('crm:leads'))   
            
            #get selected datalist
            lead_ids = request.POST.getlist('lead') 
            log.info(f'recorded {len(lead_ids)} leads!')
                            
            #If no data selected return
            if not lead_ids:
                messages.warning(request, "Please select lead")
                log.info('As no lead recorded redirecting after giving message to select the lead................')
                return HttpResponseRedirect(reverse('crm:leads'))   
            
            #Allowed limited email per action to reduce load
            if len(lead_ids) > settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME:
                messages.warning(request, f"Please select less then {settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME}! " + "There was " + str(len(request.POST.getlist('lead'))) + " selected!" )
                log.info(f'As selected lead is more than {settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME} , so that redirecting by giving message to select allowed leads............')
                return HttpResponseRedirect(reverse('crm:leads'))             
             
            
            # If no qualified lead found system will redirect.                
            result_lead = Lead.objects.filter(pk__in = lead_ids, subscribed = True) 
            log.info('recording leads whose are subscribed only...........')
            if not result_lead.exists():
                messages.warning(request, "No Subscribed lead found")
                log.info('As there is no subscribed leads found in the selected leads, we are redirecting............')
                return HttpResponseRedirect(reverse('crm:leads'))  
            
            
            process_count = 0
            pending_in_queue = 0
            log.info('Changing confirmation code of the lead to be secure from robotic actions!')
            for rl in result_lead:                
                #To protect to be unsubscribe lead by robotic action                
                pending_exists = MailQueue.objects.filter(to = rl.email_address, processed = False).count()   
                try:             
                    if not pending_exists:     
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
                except:
                    log.info(f'There was an error while trying to change the code for lead {rl}, so that going to process to the next............... ')
                    continue    
            log.info(f'Code changed to all selected subscribed leads where no error found. Total {process_count} processed out of {len(result_lead)}.......')         
                
            msg_process_to_queue = f"{process_count} Mail processed successfully in mail queue and {pending_in_queue} mail still exists in queue to sent!"     
            messages.success(request, msg_process_to_queue)
            log.info(msg_process_to_queue)
            
        '''Save lead form CSV file'''    
        if 'lead_upload' in request.FILES:    
            log.info('Uploading leads through CSV...........')        
            upload_csv_form = UploadLead(request.POST, request.FILES)            
            if upload_csv_form.is_valid():   
                log.info('upload form is valid......')             
                lead_upload = upload_csv_form.cleaned_data['lead_upload'] 
                #alow only csv
                if not lead_upload.name.endswith('.csv'):
                    messages.error(request, 'File is not CSV type! Pleas Save your excel file in .csv format')
                    log.info('file is not CSV, so redirecting...........')
                    return HttpResponseRedirect(reverse('crm:leads'))  
                
                #protect to extra large
                if lead_upload.multiple_chunks():
                    messages.error(request, 'Uploaded file is too big (%.2f MB)' %(lead_upload.size(1000*1000),))
                    log.info('File is too big, redirecting.......')
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
                log.info(f'{entry_count} leads added to the lead table and there was {error_count} error during saving.......')   
            else:
                log.info('Upload form was Invalid')  
            
    upload_csv_form = UploadLead()
    log.info('Lead upload form ready on get request.............')
    
        
    #List of Leads
    leads = Lead.objects.all().order_by('lead')
    log.info(f'Found {leads.count()} leads...........')
    
    #pagination
    page = request.GET.get('page', 1)
    log.info('Creating pagination............')
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
        'EXECUT_MAIL_IN_MIN': SendQueueMail.RUN_EVERY_MINS,
        'RETRY_AFTER_FAILURE_MINS': SendQueueMail.RETRY_AFTER_FAILURE_MINS,
        'LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME' : settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME,
        'pending_queue_count' : pending_queue_count()
        
    }
    return render(request, 'crm/leads.html', context = context)

def unsubscrib(request, **kwargs):  
    un_email = kwargs['email']
    un_code = kwargs['code']
    try:  
        lead = Lead.objects.get(email_address = un_email, confirm_code = un_code)
        lead.subscribed = False
        lead.save() 
        log.info(f'{un_email} unsubscribed from CRM mail!............')   
    except:
        messages.warning(request, "No email found or code expired!")
        log.warning(f'Unsubscribed action attempt where no {un_email} email found or code exppired!!!!!!!!!!!!!!!!!!!!')
        return HttpResponseRedirect(reverse('home:home'))        
        
        
    return render(request, 'crm/unsubscribed.html', {'lead': lead, 'action': 'unsubscribed'})

def subscrib(request, **kwargs): 
    email =  kwargs['email']  
    try:
        lead = Lead.objects.get(email_address = email)
        lead.subscribed = True
        lead.save()    
        log.info(f'{email} confirm subscription to CRM!............')  
    except Exception as e:
        messages.warning(request, "No email found!")
        log.warning(f'CRM confirmation to subscription for email {email} unsuccessfull due to {e} !')  
        return HttpResponseRedirect(reverse('home:home'))      
        
    return render(request, 'crm/subscribed.html', {'lead': lead, 'action': 'subscribed'})


             
    