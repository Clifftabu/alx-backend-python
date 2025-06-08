from datetime import datetime
from django.http import HttpResponse


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if current_hour < 9 or current_hour >= 17:
            return HttpResponse("Access restricted to working hours (9 AM - 5 PM).", status=403)
        return self.get_response(request)
