# Import necessary modules and views from Django.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.contrib import messages

# Import models and forms from the current app and other app(s).
from .models import *
from .forms import *

# Import a custom module named 'site_info' for meta information.
from doc.doc_processor import site_info

# Import the logging module for creating log entries.
import logging

# Get a logger instance named 'log'.
log = logging.getLogger('log')



class Glist(ListView):
    """
    View for displaying the glossary list and handling glossary requests.

    This class-based view extends Django's ListView and is responsible for
    rendering the glossary list, handling glossary request submissions,
    and providing additional context data.

    Attributes:
        model (Glossary): The model to query for glossary entries.
        paginate_by (int, optional): Uncomment to enable pagination with a specific number of entries per page.

    Methods:
        get_context_data: Override to provide additional context data.
        post: Handle POST requests for submitting glossary requests.
    """
    model = Glossary 
    # paginate_by = 100  # Uncomment to enable pagination with a specific number of entries per page.
   
   
    def get_context_data(self, **kwargs):  
        """
        Get additional context data for the glossary list view.

        This method overrides the base class method to provide additional
        context data for rendering the glossary list view. It includes
        a form for submitting glossary requests and meta information.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing context data.
        """
        log.info(f'Glossary accessed by {self.request.user}')    
        
          
        context = super().get_context_data(**kwargs) 
        
        # Create an instance of the GRequestForms for the request form.      
        request_form = GRequestForms()
        context['request_form'] = request_form
        
        
        # Define meta information for the page.
        meta_data = site_info()    
        meta_data['title'] = f'Glossaries'
        meta_data['description'] = f"Glossaries of green fuel validation platform and definitions."
        meta_data['tag'] = 'glossary, glosaries, gf-vp'
        meta_data['robots'] = 'index, follow'       
        
        # Add meta information to the context.
        context['site_info'] = meta_data   
    
    
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for submitting glossary requests.

        This method handles POST requests for submitting glossary requests.
        It validates the request form, saves the request if it's valid,
        and provides feedback to the user via messages.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: A response indicating the result of the request submission.
        """        
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