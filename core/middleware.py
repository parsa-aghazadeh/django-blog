from datetime import date
from django.conf import settings

class CurrentDateTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.test = 'hello'
        response = self.get_response(request)
        return response