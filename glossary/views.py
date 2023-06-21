from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from .models import *
from blog.models import BlogPost
from . forms import * 
from django.contrib import messages
from django.db.models.query import QuerySet
from doc.doc_processor import site_info

import logging
log =  logging.getLogger('log')


# Create your views here.
class Glist(ListView):
    model = Glossary 
    # paginate_by = 100  # if pagination is desired    
   
   
    def get_context_data(self, **kwargs):  
        log.info(f'Glossary accessed by {self.request.user}')      
        context = super().get_context_data(**kwargs)       
        request_form = GRequestForms()
        context['request_form'] = request_form
        
        
        #meta
        meta_data = site_info()    
        meta_data['title'] = f'Glossaries'
        meta_data['description'] = f"Glossaries of green fuel validation platform and definitions."
        meta_data['tag'] = 'glossary, glosaries, gf-vp'
        meta_data['robots'] = 'index, follow'
        # meta_data['og_image'] = self.request.user.type.icon.url 
        
        context['site_info'] = meta_data      
    
    
    
    
        return context
    
    def post(self, request, *args, **kwargs):
        
        
        request_form = GRequestForms(request.POST)
        if request_form.is_valid():
            request_form.save()     
            log.info(f'Glossary request posted by {request.user}')         
            messages.success(request, 'Request Submitted!')
        else:
            messages.error(request, 'Invalid form submission.')
            messages.error(request, request_form.errors)   
            return HttpResponseRedirect(reverse_lazy('glossary:g_list'))   
        
        return super(Glist, self).get(request, *args, **kwargs)