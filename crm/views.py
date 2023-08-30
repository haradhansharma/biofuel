import csv
from urllib.error import URLError, HTTPError
from django.db import IntegrityError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from doc.doc_processor import site_info
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
from django.template.loader import render_to_string
from .models import random_digits

import logging
log =  logging.getLogger('log')


#helper function to get ip address
def get_ip(request):
    """
    Get the user's IP address from the request.

    This helper function attempts to extract the user's IP address from various headers in the HTTP request.
    It first checks common headers like 'HTTP_X_FORWARDED_FOR', 'HTTP_CLIENT_IP', etc., to obtain the IP.
    If no valid IP is found in headers, it falls back to using 'REMOTE_ADDR'.
    
    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        str: The user's IP address.
    """
    log.info('Recording users IP............')
    
    # Check various headers to extract the user's IP address
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



def get_location_info(request):
    """
    Get location information based on the user's IP address.

    This function uses the IP address of the user obtained from the `get_ip` function to retrieve
    location details from the IPinfo database. It uses the provided API token from the settings
    to authenticate the request. The function returns location-related data, including city, region,
    country, and more.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        dict: Location-related information obtained from the IPinfo database.
    """  
    log.info('Geting Location details based on IP')
    
    # Obtain user's IP address
    ip = get_ip(request)
    
    # Get IPinfo token from settings
    token = settings.IPINFO_TOKEN    
  
    # Construct the URL for IPinfo API request
    info_url = f'https://ipinfo.io/{ip}?token={token}'
    
    data = {}
    
    try:
        # Send HTTP request to IPinfo API
        with urllib.request.urlopen(info_url) as url:
            if url.getcode() == 200:
                data = json.loads(url.read().decode())
                data.update(data)  # Update the data dictionary with IP information
                log.info(f'Location data {data} found for user {request.user}')
            else:
                log.info(f'IPinfo API returned status code {url.getcode()} for user {request.user}')
    except (URLError, HTTPError) as e:
        # Handle URL and HTTP errors
        log.error(f'Error while fetching location data for user {request.user}: {e}')    

    
    return data

  

def subscription(request):
    """
    Process subscription requests and send confirmation emails.

    This function handles subscription requests submitted through a form. It validates the
    submitted data and performs the following steps:
    - Checks if the supplied email address already exists in the Lead database.
    - If the email exists and is subscribed, returns an error indicating the email is already subscribed.
    - If the email exists but is not subscribed, sends a confirmation email for subscription.
    - If the email does not exist, saves a new Lead entry and sends a confirmation email.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response indicating the result of the subscription attempt.
    """
    # get location info of subscribes
    location_info = get_location_info(request)
    
    # prepare subscription form
    subscription_form = SubscriberForm()
    
    # Define Name
    name= None  
    
    # Define email  
    email = None   
    
    # get city if exists
    city =  location_info.get('city') 
    
    # get country if exits
    country_code = location_info.get('country')
    
    country = country_code
    
    # Get current site's information
    current_site = site_info()
    
    if request.method == 'POST':            
        if 'new_subscriber' in request.POST:
            
            subscription_form = SubscriberForm(request.POST)
            
            # Validate subscription form and collect posted data
            if subscription_form.is_valid():
                
                name = subscription_form.cleaned_data['name']                
                email = subscription_form.cleaned_data['email']
                
                confirm_url = request.build_absolute_uri(reverse('crm:subscrib', kwargs={'email': email}))                    
                
                subject = 'Please confirm your subscription!'
                
                # Render email through template
                message = render_to_string('emails/subscription_confirmation.html', {
                        'confirm_url': confirm_url,
                        'name' : name,
                        'email' : email,                                                               
                        'current_site': current_site,            
                        }) 
                
                # Define From email address
                email_from = settings.DEFAULT_FROM_EMAIL
                
                # Define To address to send mail
                email_to = [email]
                
                try:
                    lead = Lead.objects.get(email_address = email)  
                except Lead.DoesNotExist:
                    lead = None
                    
                if lead is not None:
                    if lead.subscribed:
                        # If lead already subscribed return respons through HTMX
                        return HttpResponse(f' <span class="text-danger"> The {email} already subscribed! </span>')
                    else: 
                        # Send mail aboust new subscription to the subscribe and return
                        send_mail(subject, message, email_from, email_to, html_message = message )   
                        return HttpResponse(f' <span class="text-danger"> An email for confirmation has been sent to {email} ! Please confirm! </span>')
                else:
                    try:                        
                        Lead.objects.create(lead = name, email_address=email,city=city,country=country,subscribed=False)
                        log.info(f'{email} created as new lead!')
                    except Exception as e:
                        log.warning(f'There was a problem to save {email} as new lead due to {e}')
                    
                    # Send mail aboust new subscription to the subscribe and return
                    send_mail(subject, message, email_from, email_to, html_message = message ) 
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
    """
    Display and manage leads for the CRM.

    This view function handles various lead-related actions, including lead deletion,
    adding leads to the mail queue for sending later, and uploading leads via a CSV file.
    It also provides lead pagination and associated documentation.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A rendered HTML template with lead data and related information.
    """
    # Ensure session is cleared to avoid errors
    null_session(request)   
    
    # Process POST requests  
    if request.method == "POST":  
        
        # Get selected data 
        lead_ids = request.POST.getlist('lead')
              
        # Handle lead deletion
        if 'delete_lead' in request.POST:
            
            # If no data selected return
            if not lead_ids:
                messages.warning(request, "Please select lead")
                log.info('No lead selected to delete so that redirecting.....')
                return HttpResponseRedirect(reverse('crm:leads')) 
            
            
            # Delete selected leads using bulk delete
            delete_count, _ = Lead.objects.filter(id__in=lead_ids).delete()
            messages.success(request, f"{delete_count} lead deleted successfully.")
            log.info(f"{delete_count} lead deleted successfully by {request.user}.")    
              
        # Add leads to mail queue for later sending         
        # lead to queue to sent later. settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME lead can be added at a time. it can be adjusted form setting file. But More then 50 site can be slow.
        if 'mail_lead' in request.POST:  
                      
            # If unsent more then setting value in the queue no lead will be added to the queue
            if pending_queue_count() >= settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME:
                mgs_string_for_mail_lead = f"There are {pending_queue_count()} mail in queue! The command can be proccessed if queue less then {settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME}!"
                messages.warning(request, mgs_string_for_mail_lead )
                log.info(str(mgs_string_for_mail_lead) + str('so that redirecting...........'))
                return HttpResponseRedirect(reverse('crm:leads')) 
            log.info(f'recorded {len(lead_ids)} leads!')
                            
            # If no data selected return
            if not lead_ids:
                messages.warning(request, "Please select lead")
                log.info('As no lead recorded redirecting after giving message to select the lead................')
                return HttpResponseRedirect(reverse('crm:leads'))   
            
            # Allowed limited email per action to reduce load
            if len(lead_ids) > settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME:
                messages.warning(request, f"Please select less then {settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME}! " + "There was " + str(len(request.POST.getlist('lead'))) + " selected!" )
                log.info(f'As selected lead is more than {settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME} , so that redirecting by giving message to select allowed leads............')
                return HttpResponseRedirect(reverse('crm:leads'))             
             
            
            # If no qualified lead found system will redirect.                
            result_lead = Lead.objects.filter(pk__in = lead_ids, subscribed = True) 
               
            log.info('Recording leads that are subscribed only...')
            if not result_lead.exists():
                messages.warning(request, "No subscribed leads found")
                log.info('No subscribed leads found in the selected leads, redirecting...')
                return HttpResponseRedirect(reverse('crm:leads'))
            
            
            # Check pending emails for each lead
            lead_email_set = set(rl.email_address for rl in result_lead)
            pending_counts = MailQueue.objects.filter(to__in=lead_email_set, processed=False).values('to').annotate(pending_count=Count('to'))
            
            process_count = 0
            pending_in_queue = 0
            update_data = []
            mail_queue_data = []
            
            for rl in result_lead:
                #To protect to be unsubscribe lead by robotic action                
                if rl.email_address not in (pending_count['to'] for pending_count in pending_counts):
                    confirm_code = random_digits()
                    update_data.append({'id': rl.id, 'confirm_code': confirm_code})
                    mail_queue_data.append(MailQueue(to=rl.email_address))
                    process_count += 1
                else:
                    pending_in_queue += 1

            # Bulk update confirm codes
            Lead.objects.bulk_update(update_data, ['confirm_code'])
            
            # Bulk create mail queue entries
            MailQueue.objects.bulk_create(mail_queue_data)
            
            msg_process_to_queue = f"{process_count} mail processed successfully in mail queue and {pending_in_queue} mail still in queue to be sent!"
            messages.success(request, msg_process_to_queue)
            log.info(msg_process_to_queue)   
            
            
        # Upload leads from CSV file    
        if 'lead_upload' in request.FILES:  
              
            log.info('Uploading leads through CSV...........') 
                   
            upload_csv_form = UploadLead(request.POST, request.FILES)     
                   
            if upload_csv_form.is_valid():   
                log.info('upload form is valid......')     
                        
                lead_upload = upload_csv_form.cleaned_data['lead_upload'] 
                
                # Check if the uploaded file is in CSV format
                if not lead_upload.name.endswith('.csv'):
                    messages.error(request, 'File is not in CSV format. Please save your Excel file in .csv format.')
                    log.info('File is not in CSV format, redirecting...........')
                    return HttpResponseRedirect(reverse('crm:leads'))  
                
                # Check for large file size  
                if lead_upload.multiple_chunks():
                    file_size_mb = lead_upload.size / (1024 * 1024)  # Convert file size to MB
                    messages.error(request, f"Uploaded file is too big ({file_size_mb:.2f} MB)")
                    log.info('File is too big, redirecting.......')
                    return HttpResponseRedirect(reverse('crm:leads'))                
                
                # Process the uploaded CSV data
                data = csv.DictReader(chunk.decode() for chunk in lead_upload)
                
                entry_count = 0
                error_count = 0  
                              
                for d in data:                    
                    try:
                        new_lead = Lead(
                            lead = str(d['lead']), 
                            email_address = str(d['email_address']), 
                            phone = str(d['phone']), 
                            address_1 = str(d['address_1']), 
                            address_2 = str(d['address_2']), 
                            country = str(d['country_code']), 
                            city = str(d['city'])
                            )
                        new_lead.save()
                        entry_count += 1
                    except Exception as e:
                        error_count += 1
                        
                # Display success and error messages       
                messages.success(request, f'{entry_count} lead has beed added! \n')
                messages.error(request, f"\n There was {error_count} error! Please check file format, record's title and duplicate email before each upload! \n")       
                log.info(f'{entry_count} leads added to the lead table and there was {error_count} error during saving.......')   
            else:
                messages.error(request, f"\n Upload form was Invalid \n")   
                log.error('Upload form was Invalid')  
    
    # Initialize the lead upload form        
    upload_csv_form = UploadLead()  
    
        
    # Retrieve and paginate leads
    leads = Lead.objects.all().order_by('lead')    
    page = request.GET.get('page', 1)  
    paginator = Paginator(leads, 50)
    try:
        leads = paginator.page(page)
    except PageNotAnInteger: 
        leads = paginator.page(1)
    except EmptyPage:
        leads = paginator.page(paginator.num_pages)
    
    docs = Acordion.objects.filter(apps = 'crm')
    
    # Gather meta information for the page
    meta_data = site_info()    
    meta_data['title'] = 'Leads'
    meta_data['description'] = f'This is a simple CRM for Green Fuel Validation Platform.'
    meta_data['tag'] = 'crm'
    meta_data['robots'] = 'noindex, nofollow'

    # Prepare the context for rendering the template
    context = {        
        'leads': leads,
        'upload_csv_form': upload_csv_form,
        'docs': docs,
        'EXECUT_MAIL_IN_MIN': SendQueueMail.RUN_EVERY_MINS,
        'RETRY_AFTER_FAILURE_MINS': SendQueueMail.RETRY_AFTER_FAILURE_MINS,
        'LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME' : settings.LEAD_MAIL_SEND_FROM_QUEUE_AT_A_TIME,
        'pending_queue_count' : pending_queue_count(),
        'site_info' : meta_data  
        
    }
    return render(request, 'crm/leads.html', context = context)



def unsubscrib(request, **kwargs):  
    """
    Unsubscribe a lead from receiving further CRM emails.

    This function processes an unsubscribe request by verifying the provided email
    and confirmation code against the `Lead` model. If the email and code match,
    the lead's subscription status is set to `False`, effectively unsubscribing them
    from receiving further CRM emails.

    Args:
        request (HttpRequest): The HTTP request object.
        **kwargs: Keyword arguments containing 'email' and 'code' from the URL.

    Returns:
        HttpResponse: A rendered HTML template confirming the unsubscribed status
                      for the lead, or an error message if the email or code is invalid.
    """
    
    # Get email and confirmation code from URL parameters
    un_email = kwargs['email']
    un_code = kwargs['code']
    
    try:  
        # Attempt to find the lead based on email and confirmation code
        lead = Lead.objects.get(email_address = un_email, confirm_code = un_code)
        
        # Unsubscribe the lead by setting 'subscribed' to False
        lead.subscribed = False
        lead.save() 
        
        # Log the unsubscribe action
        log.info(f'{un_email} unsubscribed from CRM mail!............')   
        
    except:
        # Handle invalid email or expired code
        messages.warning(request, "No email found or code expired!")
        log.warning(f'Unsubscribed action attempt where no {un_email} email found or code exppired!')
        
        # Redirect to home page with a warning message
        return HttpResponseRedirect(reverse('home:home'))   
    
    # Render the 'unsubscribed' template with lead information   
    return render(request, 'crm/unsubscribed.html', {'lead': lead, 'action': 'unsubscribed'})

def subscrib(request, **kwargs): 
    """
    Confirm Subscription Function
    
    This view handles the confirmation of a lead's subscription to the CRM. It is accessed via a confirmation link sent in emails.
    
    Args:
        request (HttpRequest): The HTTP request object.
        **kwargs: Keyword arguments containing 'email' from the URL.

    Returns:
        HttpResponse: A rendered HTML template confirming the subscription status for the lead or an error message if the email is invalid.
    """
    
    # Extract email from URL parameters
    email =  kwargs['email']  
    
    try:
        # Attempt to find the lead with the provided email
        lead = Lead.objects.get(email_address = email)
        
        # Set the 'subscribed' field to True and save the lead
        lead.subscribed = True
        lead.save()    
        
        log.info(f'{email} confirm subscription to CRM!............')  
        
    except Exception as e:
        # Handle exceptions if lead not found
        messages.warning(request, "No email found!")
        log.warning(f'CRM confirmation to subscription for email {email} unsuccessfull due to {e} !')  
        
        # Redirect to the home page
        return HttpResponseRedirect(reverse('home:home'))     
    
    # Render the subscribed confirmation template        
    return render(request, 'crm/subscribed.html', {'lead': lead, 'action': 'subscribed'})


             
    