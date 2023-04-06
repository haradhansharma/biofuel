from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Feedback
from django.http import HttpResponse
import requests


def submit_feedback(request):
    
    # url = request.build_absolute_uri()
    # response = requests.get(url)
    # content = response.content.decode('utf-8')
    
    # print(content)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
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