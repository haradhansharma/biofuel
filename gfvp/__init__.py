
def null_session(request):
    '''
    It is necessary in the view where login required
    `interested_in` parameter to control registering user type
    if user autheticated then it can make trouble.
    '''
    if 'interested_in' in request.session:
        request.session['interested_in'] = None   
        
    if request.user.is_authenticated:
            try:
                del request.session['interested_in']
            except Exception as e:
                pass
                
