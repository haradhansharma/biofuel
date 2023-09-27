# from django.core.exceptions import PermissionDenied
# from django.http.response import Http404, HttpResponseRedirect, HttpResponse
# from django.urls.base import reverse
# from django.contrib import messages

# # Funtion protector to access by user type of expert or staff or superuser
# def expert_required(function):
#     def wrap(request, *args, **kwargs):
#         if request.user.is_expert or request.user.is_staff or request.user.is_superuser:
#             return function(request, *args, **kwargs)
#         else:            
#             raise PermissionDenied
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__                
#     return wrap 


# # Funtion protector to access by user type of producer or staff or superuser
# def producer_required(function):
#     def wrap(request, *args, **kwargs):        
#         if request.user.is_producer or request.user.is_staff or request.user.is_superuser:
#             return function(request, *args, **kwargs)
#         else:            
#             raise PermissionDenied
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__                
#     return wrap



# # Funtion protector to access by user type of consumer or staff or superuser
# def consumer_required(function):
#     def wrap(request, *args, **kwargs):
#         if request.user.is_consumer or request.user.is_staff or request.user.is_superuser:
#             return function(request, *args, **kwargs)
#         else:            
#             raise PermissionDenied
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__                
#     return wrap


# # Funtion protector to access by user type of marine or staff or superuser
# def marine_required(function):
#     def wrap(request, *args, **kwargs):
#         if request.user.is_marine or request.user.is_staff or request.user.is_superuser:
#             return function(request, *args, **kwargs)
#         else:            
#             raise PermissionDenied
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__                
#     return wrap

# # Funtion protector to access by reprot creator only.
# def report_creator_required(function):
#     from evaluation.models import Evaluator    
#     def wrap(request, *args, **kwargs):
#         report_user = Evaluator.objects.get(slug = kwargs['slug']).creator
#         if report_user == request.user or request.user.is_staff or request.user.is_superuser:
#             return function(request, *args, **kwargs)
#         else:            
#             raise PermissionDenied
#     wrap.__doc__ = function.__doc__
#     wrap.__name__ = function.__name__                
#     return wrap



from django.core.exceptions import PermissionDenied
from django.contrib import messages

def user_type_required(*user_types):
    """
    Decorator factory that creates a decorator for checking user types.

    Args:
        *user_types: Variable number of user types to check.

    Returns:
        A decorator that checks if the user has any of the specified user types or is staff or superuser.
    """
    def decorator(function):
        def wrap(request, *args, **kwargs):
            """
            Wrapper function that checks user type permissions before executing the view function.
            """
            if any(getattr(request.user, f'is_{user_type}') for user_type in user_types) or request.user.is_staff or request.user.is_superuser:
                return function(request, *args, **kwargs)
            else:
                raise PermissionDenied
        wrap.__doc__ = function.__doc__
        wrap.__name__ = function.__name__
        return wrap
    return decorator

expert_required = user_type_required('expert')
producer_required = user_type_required('producer')
consumer_required = user_type_required('consumer')
marine_required = user_type_required('marine')



def expert_or_producer_requried(function):
    def wrap(request, *args, **kwargs):
    
        # Check if either @expert_required or @producer_required is applied
        if request.user.is_staff or request.user.is_superuser or request.user.is_expert or request.user.is_producer:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied("Permission Denied")
        
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__                
    return wrap

def creator_or_consumer_requried(function):
    from evaluation.models import Evaluator   
    def wrap(request, *args, **kwargs):
    
        report_user = Evaluator.objects.get(slug=kwargs['slug']).creator
        if report_user == request.user or request.user.is_staff or request.user.is_superuser or request.user.is_consumer:
            return function(request, *args, **kwargs)
        else:            
            raise PermissionDenied
        
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__                
    return wrap


def report_creator_required(function):
    """
    Decorator that restricts access to the view function based on the report creator or staff/superuser.

    Args:
        function: The view function to be decorated.

    Returns:
        The decorated view function that checks for report creator or staff/superuser permissions.
    """
    from evaluation.models import Evaluator    
    def wrap(request, *args, **kwargs):
        """
        Wrapper function that checks if the current user is the report creator or is staff/superuser.
        """
        report_user = Evaluator.objects.get(slug=kwargs['slug']).creator
        if report_user == request.user or request.user.is_staff or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:            
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__                
    return wrap





