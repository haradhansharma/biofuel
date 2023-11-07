from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from crm.views import get_ip
from .models import ConsentRecord

def cookie_consent(request):
    """
    Handles user consent for cookies and stores the consent record in the database.

    This view checks whether a user has accepted or declined cookie usage.
    It creates a ConsentRecord object to store information about the user's decision.
    If the user accepts cookies, a 'cookie_consent' cookie is set with a one-year expiration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: An HTTP response, either a redirection to the referring page or a rendered consent page.
    """
    referer = request.META.get('HTTP_REFERER', reverse('home:home'))
    
    if request.method == 'POST':
        consent = request.POST.get('consent')
        response = HttpResponseRedirect(referer)
        
        session_id = request.session.session_key
        ip = get_ip(request)
        
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        
        if consent == 'accept':
            response.set_cookie('cookie_consent', 'accepted', max_age=31536000)
            consent_type = 'accept'
        elif consent == 'decline':
            response.delete_cookie('cookie_consent')  # Remove the cookie when consent is declined
            consent_type = 'decline'
            
        ConsentRecord.objects.create(
            user = user,
            session_id = session_id,
            ip = ip,
            consent_type = consent_type            
        )

        return response

    return render(request, 'gf_cookies/cookie_consent.html')