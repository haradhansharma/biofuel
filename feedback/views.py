from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Feedback
from django.http import HttpResponse
from doc.doc_processor import site_info

import logging


# Initialize a logger instance.
log =  logging.getLogger('log')


def submit_feedback(request):   
    
    """
    View for handling user feedback submission.

    This view function processes feedback submissions. It handles both GET and POST requests.
    When a POST request is made with valid feedback data, it saves the feedback, logs the action,
    and returns a success message. For GET requests, it pre-fills the feedback form with
    relevant data.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response indicating success or a form for feedback submission.
    """
    
    # Get site information (assuming you have a 'site_info' function). 
    site = site_info()  
    
    if request.method == 'POST':
        # Handle the POST request for submitting feedback.
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            if request.user.is_authenticated:
                # Log the feedback submission with the authenticated user's name.
                log.info(f"Feedback Saved by_____________ {request.user}. visit: http://{site.get('domain')}/admin/feedback/feedback/{feedback.pk}/change/ to see!")   
            else:
                # Log the feedback submission with the user's email (if not authenticated).
                log.info(f"Feedback saved by________________{form.cleaned_data['email']}. visit: http://{site.get('domain')}/admin/feedback/feedback/{feedback.pk}/change/ to see!")
            return HttpResponse('<div class="alert alert-primary" role="alert">Feedback Received! Thank you!</div>')
    else:
        # Handle the GET request to pre-fill the feedback form.
        initial_dict = {
            "url" : request.META.get('HTTP_REFERER'),
            "email" : request.user.email if request.user.is_authenticated else '',
            "name" : request.user.get_full_name if request.user.is_authenticated else '',
            "phone" : request.user.phone if request.user.is_authenticated else '',           
            
            }
        form = FeedbackForm(initial = initial_dict)
    # Render the feedback submission form.
    return render(request, 'feedback/submit.html', {'form': form})