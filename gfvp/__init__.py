import logging
log =  logging.getLogger('log')
def null_session(request):
    
    if 'interested_in' in request.session:
        request.session['interested_in'] = None   
        
    if request.user.is_authenticated:
            try:
                del request.session['interested_in']
            except Exception as e:
                pass
                