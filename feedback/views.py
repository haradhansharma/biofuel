from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Feedback
from django.http import HttpResponse
from doc.doc_processor import site_info

import logging
log =  logging.getLogger('log')


def submit_feedback(request):    
    site = site_info()  
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            if request.user.is_authenticated:
                log.info(f"Feedback Saved by_____________ {request.user}. visit: http://{site.get('domain')}/admin/feedback/feedback/{feedback.pk}/change/ to see!")   
            else:
                log.info(f"Feedback saved by________________{form.changed_data['email']}. visit: http://{site.get('domain')}/admin/feedback/feedback/{feedback.pk}/change/ to see!")
            return HttpResponse('<div class="alert alert-primary" role="alert">Feedback Received! Thank you!</div>')
    else:
        initial_dict = {
            "url" : request.META.get('HTTP_REFERER'),
            "email" : request.user.email if request.user.is_authenticated else '',
            "name" : request.user.get_full_name if request.user.is_authenticated else '',
            "phone" : request.user.phone if request.user.is_authenticated else '',           
            
            }
        form = FeedbackForm(initial = initial_dict)
    return render(request, 'feedback/submit.html', {'form': form})