import logging
import datetime
import re
from django.http import HttpResponse



logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.datetime.now().time()
        if current_time.hour < 9 or current_time.hour >= 17:
            return HttpResponse("Access denied: allowed between 9 AM and 5 PM.")
        return self.get_response(request)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        method = request.method
        path = request.get_full_path()
        with open("requests.log", "a") as f:
            f.write(f"{datetime.datetime.now()} - {method} {path}\n")
        return self.get_response(request)
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.offensive_words = ['badword1', 'badword2', 'offensive']  # customize as needed

    def __call__(self, request):
        if request.method == 'POST':
            body = request.body.decode('utf-8')
            if any(re.search(rf'\b{word}\b', body, re.IGNORECASE) for word in self.offensive_words):
                return HttpResponse("Offensive language detected. Request blocked.", status=403)
        return self.get_response(request)

