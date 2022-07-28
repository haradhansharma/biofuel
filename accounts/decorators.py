from django.core.exceptions import PermissionDenied
from django.http.response import Http404, HttpResponseRedirect, HttpResponse
from django.urls.base import reverse
from django.contrib import messages

# Funtion protector to access by user type of expert or staff or superuser
def expert_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_expert or request.user.is_staff or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:            
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__                
    return wrap 


# Funtion protector to access by user type of producer or staff or superuser
def producer_required(function):
    def wrap(request, *args, **kwargs):        
        if request.user.is_producer or request.user.is_staff or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:            
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__                
    return wrap



# Funtion protector to access by user type of consumer or staff or superuser
def consumer_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_consumer or request.user.is_staff or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:            
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__                
    return wrap


# Funtion protector to access by user type of marine or staff or superuser
def marine_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_marine or request.user.is_staff or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:            
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__                
    return wrap

# Funtion protector to access by reprot creator only.
def report_creator_required(function):
    from evaluation.models import Evaluator    
    def wrap(request, *args, **kwargs):
        report_user = Evaluator.objects.get(slug = kwargs['slug']).creator
        if report_user == request.user or request.user.is_staff or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:            
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__                
    return wrap


