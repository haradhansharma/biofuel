from django.shortcuts import redirect
from django.conf import settings
from django.http import HttpResponse

class EvaMiddleware:  
    def __init__(self, get_response):       
        self.get_response = get_response
    def __call__(self, request):          
        res = HttpResponse('<h1 style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);">BAD REQUEST 401 </h1>')        
        try:       
            if settings.CNN == True:
                if request.path != '/':                 
                   return res 
            else:
                pass    
        except:
            return res            
                        
        if 'evaluator' not in request.session:
            request.session['evaluator'] = ''         
        response = self.get_response(request)       
        return response
    
    
        
        

        