import logging
import datetime
import re
from django.http import HttpResponse

# Logging configuration
logging.basicConfig(
    filename='requests.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Task 1: Restrict access by time middleware
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.datetime.now().time()
        if current_time.hour < 9 or current_time.hour >= 17:
            return HttpResponse("Access denied: allowed between 9 AM and 5 PM.")
        return self.get_response(request)

# Task 2: Request logging middleware
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        method = request.method
        path = request.get_full_path()
        with open("requests.log", "a") as f:
            f.write(f"{datetime.datetime.now()} - {method} {path}\n")
        return self.get_response(request)

# Task 3: Offensive language detection middleware
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.offensive_words = ['badword1', 'badword2', 'offensive']  # Customize as needed

    def __call__(self, request):
        if request.method == 'POST':
            body = request.body.decode('utf-8', errors='ignore')
            if any(re.search(rf'\b{word}\b', body, re.IGNORECASE) for word in self.offensive_words):
                return HttpResponse("Offensive language detected. Request blocked.", status=403)
        return self.get_response(request)

# Task 4: Role-based permission middleware (must be named RolepermissionMiddleware)
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.protected_paths = {
            '/admin-only/': ['admin'],
            '/moderator-only/': ['admin', 'moderator'],
        }

    def __call__(self, request):
        path = request.path
        user = getattr(request, 'user', None)

        for protected_path, allowed_roles in self.protected_paths.items():
            if path.startswith(protected_path):
                if not user or not user.is_authenticated:
                    return HttpResponse('Authentication required.', status=401)

                user_role = getattr(user, 'role', 'user')  # Default to 'user'
                if user_role not in allowed_roles:
                    return HttpResponse('Permission denied.', status=403)

        return self.get_response(request)
