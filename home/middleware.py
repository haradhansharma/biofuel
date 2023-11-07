from django.http import HttpResponsePermanentRedirect

class HttpsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.is_secure():
            url = request.build_absolute_uri().replace("http://", "https://")
            return HttpResponsePermanentRedirect(url)
        return self.get_response(request)