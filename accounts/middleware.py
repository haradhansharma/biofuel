from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


   
    
class ServiceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        if request.user.is_expert and not request.META.get('HTTP_HX_REQUEST'):
            # Check if user has selected a category
            if not request.user.selected_activities:
                forward_path = reverse('partner_service', args=[str(request.user.pk)])
                if request.path != forward_path:
                    messages.warning(request, 'Please select services you provide!')                    
                    # Redirect user to category selection page
                    return redirect(forward_path)
                else:
                    messages.warning(request, 'Please select services you provide!')   

        return self.get_response(request)


    
        
        

        